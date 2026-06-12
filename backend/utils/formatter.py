def format_review(review: dict) -> str:
    parts = ["## AI Code Review Summary", ""]
    if review.get("summary"):
        parts.append(f"**Summary:** {review['summary']}")
        parts.append("")

    if review.get("issues"):
        parts.append("**Issues:**")
        for idx, issue in enumerate(review["issues"], start=1):
            parts.append(f"{idx}. {issue}")
        parts.append("")

    if review.get("suggestions"):
        parts.append("**Suggestions:**")
        for suggestion in review["suggestions"]:
            parts.append(f"- {suggestion}")

    return "\n".join(parts)
