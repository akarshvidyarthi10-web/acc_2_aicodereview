from services.github_service import get_pr_files
from utils.formatter import format_review


async def analyze_code(diff: str) -> dict:
    prompt = f"""
You are a senior developer.
Review this code diff and provide:
- summary
- issues
- suggestions

Diff:
{diff}
"""

    # TODO: wire this to AWS Bedrock / Bedrock SDK
    # For now, return a placeholder response.
    review = {
        "summary": "Automated review generated.",
        "issues": ["No issues detected in placeholder review."],
        "suggestions": ["Replace this placeholder with Bedrock integration."],
        "comment": format_review({
            "summary": "Automated review generated.",
            "issues": ["No issues detected in placeholder review."],
            "suggestions": ["Replace this placeholder with Bedrock integration."]
        })
    }
    return review
