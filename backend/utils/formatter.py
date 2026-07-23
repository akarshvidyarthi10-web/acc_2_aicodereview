def format_review(review: dict) -> str:
    parts = ["# AI Code Review Report", ""]

    if review.get("summary"):
        parts.append("## Summary")
        parts.append(review["summary"])
        parts.append("")

    if review.get("security"):
        parts.append("## Security Issues")
        severity_groups = {"HIGH": [], "MEDIUM": [], "LOW": []}
        for item in review["security"]:
            severity = item.get("severity", "MEDIUM").upper()
            text = f"- {item.get('issue', 'Issue detected')} in {item.get('file', 'unknown')}:{item.get('line', '?')} - {item.get('suggestion', '')}"
            severity_groups.setdefault(severity, []).append(text)
        for level in ["HIGH", "MEDIUM", "LOW"]:
            if severity_groups.get(level):
                parts.append(f"### {level}")
                parts.extend(severity_groups[level])
                parts.append("")

    if review.get("smells"):
        parts.append("## Code Smells")
        for item in review["smells"]:
            parts.append(f"- {item.get('issue', 'Code smell')} in {item.get('file', 'unknown')}:{item.get('line', '?')} - {item.get('suggestion', '')}")
        parts.append("")

    if review.get("naming"):
        parts.append("## Naming Issues")
        for item in review["naming"]:
            parts.append(f"- {item.get('issue', 'Naming issue')} in {item.get('file', 'unknown')}:{item.get('line', '?')} - {item.get('suggestion', '')}")
        parts.append("")

    if review.get("suggestions"):
        parts.append("## Suggestions")
        for idx, suggestion in enumerate(review["suggestions"], start=1):
            parts.append(f"{idx}. {suggestion}")
        parts.append("")

    if review.get("review_score") is not None:
        parts.append("## Score")
        parts.append(f"{review['review_score']}/100")
        parts.append("")

    if review.get("model") or review.get("processing_time"):
        parts.append("## Model Info")
        if review.get("model"):
            parts.append(f"- Model: {review['model']}")
        if review.get("processing_time"):
            parts.append(f"- Processing time: {review['processing_time']}")

    return "\n".join(parts)
