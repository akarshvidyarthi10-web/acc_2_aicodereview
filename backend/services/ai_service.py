import json
import re
import time
import traceback

from config.settings import settings
from graphs.review_graph import run_review
from utils.formatter import format_review
from utils.logger import logger


def build_fallback_review(diff: str) -> dict:
    """Create a deterministic review when Gemini quota or API errors block AI analysis."""
    security = []
    smells = []
    naming = []
    suggestions = []

    if re.search(r"(SELECT|INSERT|UPDATE|DELETE).*(user|query|name)|\+.*query.*user|\+.*name=.*user", diff, re.I):
        security.append(
            {
                "severity": "HIGH",
                "file": "unknown",
                "line": 1,
                "issue": "Potential SQL injection risk detected in query construction.",
                "suggestion": "Use parameterized queries or ORM methods instead of concatenating user input.",
            }
        )
    if re.search(r"\b(exec|eval|subprocess|os\.system|pickle\.loads)\b", diff):
        security.append(
            {
                "severity": "HIGH",
                "file": "unknown",
                "line": 1,
                "issue": "Dynamic code execution pattern may allow command injection.",
                "suggestion": "Avoid using exec/eval or shell commands with untrusted input.",
            }
        )
    if re.search(r"TODO|FIXME|HACK|temporary|quick fix", diff, re.I):
        smells.append(
            {
                "severity": "MEDIUM",
                "file": "unknown",
                "line": 1,
                "issue": "Temporary or workaround code may reduce maintainability.",
                "suggestion": "Replace temporary markers with a proper long-term fix.",
            }
        )
    if re.search(r"\bimport os\b", diff):
        suggestions.append(
            {
                "severity": "LOW",
                "file": "unknown",
                "line": 1,
                "issue": "Unused or unnecessary import may indicate cleanup is needed.",
                "suggestion": "Remove unused imports and keep the diff focused.",
            }
        )

    score = 100
    for issue in security:
        score -= 15 if issue.get("severity") == "HIGH" else 5
    for issue in smells:
        score -= 5 if issue.get("severity") == "HIGH" else 3
    for issue in naming:
        score -= 2
    for issue in suggestions:
        score -= 1
    score = max(0, min(100, score))

    summary = (
        "Fallback review generated because the Gemini API did not complete the analysis. "
        "The diff should still be checked for security and maintainability issues."
    )

    return {
        "summary": summary,
        "security": security,
        "smells": smells,
        "naming": naming,
        "suggestions": suggestions,
        "review_score": score,
        "model": settings.gemini_model or settings.gemini_model_fallback or "fallback-review",
        "review_version": "v2-fallback",
    }


async def analyze_code(diff: str) -> dict:
    """
    Analyze code using multi-agent LangGraph workflow.
    
    Returns structured review with:
    - summary
    - security issues with severity
    - code smells with severity  
    - naming issues with suggestions
    - best practice suggestions
    - review_score (0-100)
    """
    start_time = time.perf_counter()
    logger.info("AI stage=analyze_code diff_chars=%s started", len(diff))

    try:
        result = await run_review(diff)

        elapsed = time.perf_counter() - start_time
        result["model"] = settings.gemini_model or settings.gemini_model_fallback or "fallback-review"
        result["processing_time"] = f"{elapsed:.2f}s"
        result["review_version"] = "v2-langgraph"
        result["comment"] = format_review(result)

        logger.info(
            "AI stage=analyze_code completed review_score=%s comment_len=%s elapsed=%s",
            result.get("review_score", 0),
            len(result.get("comment", "")),
            f"{elapsed:.2f}s",
        )
        return result

    except Exception as e:
        logger.exception("AI stage=analyze_code failed: %s", e)
        elapsed = time.perf_counter() - start_time
        review = build_fallback_review(diff)
        review["processing_time"] = f"{elapsed:.2f}s"
        review["model"] = settings.gemini_model or settings.gemini_model_fallback or "fallback-review"
        review["comment"] = format_review(review)
        logger.warning(
            "AI stage=analyze_code using fallback review because=%s",
            str(e),
        )
        return review

