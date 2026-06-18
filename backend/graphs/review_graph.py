"""
LangGraph review orchestrator: Coordinates multi-agent code review workflow.
- Sequential execution of all agents (simplified)
- Review score calculation
- Result aggregation
"""
import asyncio
import json
import time
import traceback
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.best_practice_agent import best_practice_agent
from agents.naming_agent import naming_agent
from agents.security_agent import security_agent
from agents.smell_agent import smell_agent
from agents.summary_agent import summary_agent
from utils.logger import logger


class ReviewState(TypedDict):
    """State object passed through the graph."""
    diff: str
    security: list
    smells: list
    naming: list
    suggestions: list
    summary: str
    recommendation: str
    review_score: int


def calculate_review_score(
    security_issues: list,
    code_smells: list,
    naming_issues: list,
    best_practice_issues: list
) -> int:
    """
    Calculate review score from 100.
    - Start: 100
    - High issue: -15
    - Medium issue: -5
    - Low issue: -2
    """
    score = 100
    
    # Security issues (highest weight)
    for issue in security_issues:
        if issue.get("severity") == "HIGH":
            score -= 15
        elif issue.get("severity") == "MEDIUM":
            score -= 5
        else:  # LOW
            score -= 2
    
    # Code smells
    for issue in code_smells:
        if issue.get("severity") == "HIGH":
            score -= 10
        elif issue.get("severity") == "MEDIUM":
            score -= 3
        else:  # LOW
            score -= 1
    
    # Naming issues (lighter)
    for issue in naming_issues:
        if issue.get("severity") == "MEDIUM":
            score -= 2
        else:  # LOW
            score -= 1
    
    # Best practice issues
    for issue in best_practice_issues:
        if issue.get("severity") == "MEDIUM":
            score -= 3
        else:  # LOW
            score -= 1
    
    # Ensure score is between 0 and 100
    return max(0, min(100, score))


async def run_all_agents_parallel(state: ReviewState) -> ReviewState:
    """Run all analysis agents sequentially to avoid overwhelming the Gemini API."""
    logger.info("LangGraph node=agents started diff_chars=%s", len(state.get("diff", "")))

    agent_calls = [
        ("security_agent", security_agent),
        ("smell_agent", smell_agent),
        ("naming_agent", naming_agent),
        ("best_practice_agent", best_practice_agent),
    ]

    results = {}
    for name, agent_fn in agent_calls:
        try:
            result = await agent_fn(state["diff"])
            results[name] = result
            logger.info("LangGraph node=%s completed type=%s", name, type(result).__name__)
        except Exception:
            logger.exception("LangGraph node=%s failed", name)
            results[name] = {}

    sec = results.get("security_agent", {})
    sml = results.get("smell_agent", {})
    nam = results.get("naming_agent", {})
    bst = results.get("best_practice_agent", {})

    state["security"] = sec.get("security", []) if isinstance(sec, dict) else []
    state["smells"] = sml.get("smells", []) if isinstance(sml, dict) else []
    state["naming"] = nam.get("naming", []) if isinstance(nam, dict) else []
    state["suggestions"] = bst.get("suggestions", []) if isinstance(bst, dict) else []

    logger.info(
        "LangGraph node=agents completed security=%s smells=%s naming=%s suggestions=%s",
        len(state["security"]),
        len(state["smells"]),
        len(state["naming"]),
        len(state["suggestions"]),
    )
    return state


async def run_summary_agent_node(state: ReviewState) -> ReviewState:
    """Execute summary agent with context from other agents."""
    logger.info("LangGraph node=summary_agent started")
    try:
        result = await summary_agent(
            state["diff"],
            security_issues=state.get("security", []),
            code_smells=state.get("smells", []),
            naming_issues=state.get("naming", []),
            best_practice_issues=state.get("suggestions", []),
        )
        state["summary"] = result.get("summary", "")
        state["recommendation"] = result.get("recommendation", "COMMENT")
        logger.info(
            "LangGraph node=summary_agent completed recommendation=%s summary_len=%s",
            state["recommendation"],
            len(state["summary"]),
        )
    except Exception as exc:
        logger.exception("LangGraph node=summary_agent failed: %s", exc)
        state["summary"] = "Review generation failed."
        state["recommendation"] = "COMMENT"
    return state


async def calculate_score(state: ReviewState) -> ReviewState:
    """Calculate final review score."""
    logger.info("LangGraph node=score started")
    score = calculate_review_score(
        state.get("security", []),
        state.get("smells", []),
        state.get("naming", []),
        state.get("suggestions", []),
    )
    state["review_score"] = score
    logger.info("LangGraph node=score completed score=%s", score)
    return state


def build_review_graph():
    """Build the LangGraph for multi-agent review."""
    workflow = StateGraph(ReviewState)
    
    # Add nodes - use async functions directly
    workflow.add_node("agents", run_all_agents_parallel)
    workflow.add_node("summary", run_summary_agent_node)
    workflow.add_node("score", calculate_score)
    
    # Build edges - sequential flow
    workflow.add_edge(START, "agents")
    workflow.add_edge("agents", "summary")
    workflow.add_edge("summary", "score")
    workflow.add_edge("score", END)
    
    return workflow.compile()


async def run_review(diff: str) -> dict:
    """
    Execute the complete multi-agent review workflow.
    
    Args:
        diff: GitHub PR diff text
        
    Returns:
        Structured review with security, smells, naming, suggestions, score
    """
    graph = build_review_graph()
    
    initial_state = {
        "diff": diff,
        "security": [],
        "smells": [],
        "naming": [],
        "suggestions": [],
        "summary": "",
        "recommendation": "",
        "review_score": 0,
    }
    
    logger.info("Starting LangGraph review for diff_chars=%s", len(diff))
    start = time.time()

    final_state = await graph.ainvoke(initial_state)

    elapsed = time.time() - start
    logger.info("LangGraph review completed in %.2fs", elapsed)

    return {
        "summary": final_state.get("summary", ""),
        "recommendation": final_state.get("recommendation", "COMMENT"),
        "security": final_state.get("security", []),
        "smells": final_state.get("smells", []),
        "naming": final_state.get("naming", []),
        "suggestions": final_state.get("suggestions", []),
        "review_score": final_state.get("review_score", 0),
    }


# Export graph for potential LangServe
graph = build_review_graph()

