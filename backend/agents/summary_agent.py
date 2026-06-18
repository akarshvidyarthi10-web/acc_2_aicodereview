"""
Summary Agent: Generates overall assessment and summary.
- Overall quality score
- Key findings summary
- Approval recommendation
"""
import json
from typing import TypedDict
from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class SummaryAgentOutput(TypedDict):
    summary: str
    recommendation: str


async def summary_agent(
    diff: str, 
    security_issues: list = None,
    code_smells: list = None,
    naming_issues: list = None,
    best_practice_issues: list = None,
    review_context: dict = None
) -> SummaryAgentOutput:
    """Generate summary and overall assessment."""
    
    # Prepare context about existing issues
    issues_summary = f"""
Security Issues: {len(security_issues or [])}
Code Smells: {len(code_smells or [])}
Naming Issues: {len(naming_issues or [])}
Best Practice Issues: {len(best_practice_issues or [])}

High Severity Issues: {sum(1 for issue in (security_issues or []) if issue.get('severity') == 'HIGH')}
"""
    
    prompt = f"""You are a senior code review expert. Provide an executive summary of this PR.

Current issues found:
{issues_summary}

Return ONLY a JSON object (no other text) with this structure:
{{
  "summary": "1-2 sentence overall assessment of the PR quality and main findings",
  "recommendation": "APPROVE|REQUEST_CHANGES|COMMENT - based on severity of issues"
}}

Diff:
{diff}

Return ONLY valid JSON, nothing else."""

    try:
        model_name = settings.gemini_model or settings.gemini_model_fallback or "gemini-1.5-flash"
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            api_key=settings.gemini_api_key,
            temperature=0,
        )

        response = llm.invoke(prompt)
        content = response if isinstance(response, str) else getattr(response, "content", str(response))
        
        # Extract JSON from response
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(content[start:end])
            else:
                result = {"summary": "Review completed.", "recommendation": "COMMENT"}
        
        return SummaryAgentOutput(
            summary=result.get("summary", "Review completed."),
            recommendation=result.get("recommendation", "COMMENT")
        )
    
    except Exception as e:
        print(f"Summary agent error: {e}")
        return SummaryAgentOutput(
            summary="Review completed with errors.",
            recommendation="COMMENT"
        )
