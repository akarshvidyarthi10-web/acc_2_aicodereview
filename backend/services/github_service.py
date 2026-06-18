import httpx

from config.settings import settings
from utils.logger import logger

GITHUB_API_URL = "https://api.github.com"


async def get_pr_files(repo: str, pr_number: int):
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }
    logger.info("GitHub API stage=get_pr_files repo=%s pr=%s url=%s", repo, pr_number, url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        logger.info(
            "GitHub API stage=get_pr_files repo=%s pr=%s status=%s",
            repo,
            pr_number,
            response.status_code,
        )
        response.raise_for_status()
        return response.json()


async def get_pr_details(repo: str, pr_number: int):
    """Get PR details including commit SHA."""
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }
    logger.info("GitHub API stage=get_pr_details repo=%s pr=%s", repo, pr_number)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        logger.info(
            "GitHub API stage=get_pr_details repo=%s pr=%s status=%s",
            repo,
            pr_number,
            response.status_code,
        )
        response.raise_for_status()
        return response.json()


async def post_comment(repo: str, pr_number: int, review: dict):
    """Post a single review comment on the PR."""
    url = f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }
    body = {
        "body": review.get("comment", "AI review result is ready.")
    }
    logger.info(
        "GitHub API stage=post_comment repo=%s pr=%s body_len=%s",
        repo,
        pr_number,
        len(body["body"]),
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        logger.info(
            "GitHub API stage=post_comment repo=%s pr=%s status=%s",
            repo,
            pr_number,
            response.status_code,
        )
        response.raise_for_status()
        return response.json()


async def post_review_with_inline_comments(
    repo: str,
    pr_number: int,
    review: dict,
    commit_sha: str,
):
    """
    Post a GitHub review with inline comments for each issue.
    """
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }

    comments = []

    for issue in review.get("security", []):
        if issue.get("line") and issue.get("file"):
            comments.append(
                {
                    "path": issue["file"],
                    "line": issue["line"],
                    "side": "RIGHT",
                    "body": f"🔒 **[{issue.get('severity', 'MEDIUM')}] Security Issue**\n\n{issue.get('issue', '')}\n\n💡 {issue.get('suggestion', '')}",
                }
            )

    for issue in review.get("smells", []):
        if issue.get("line") and issue.get("file"):
            comments.append(
                {
                    "path": issue["file"],
                    "line": issue["line"],
                    "side": "RIGHT",
                    "body": f"👃 **[{issue.get('severity', 'MEDIUM')}] Code Smell**\n\n{issue.get('issue', '')}\n\n💡 {issue.get('suggestion', '')}",
                }
            )

    for issue in review.get("naming", []):
        if issue.get("line") and issue.get("file"):
            comments.append(
                {
                    "path": issue["file"],
                    "line": issue["line"],
                    "side": "RIGHT",
                    "body": f"📝 **Naming Issue**\n\n{issue.get('issue', '')}\n\n💡 {issue.get('suggestion', '')}",
                }
            )

    if not comments:
        return await post_comment(repo, pr_number, review)

    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/reviews"
    review_body = {
        "commit_id": commit_sha,
        "body": f"🤖 **AI Code Review** - Score: {review.get('review_score', 0)}/100\n\n{review.get('summary', 'Review completed.')}",
        "event": "COMMENT",
        "comments": comments[:30],
    }
    logger.info(
        "GitHub API stage=post_review_with_inline_comments repo=%s pr=%s comment_count=%s",
        repo,
        pr_number,
        len(comments),
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=review_body)
        logger.info(
            "GitHub API stage=post_review_with_inline_comments repo=%s pr=%s status=%s",
            repo,
            pr_number,
            response.status_code,
        )
        response.raise_for_status()
        return response.json()

