from services.github_service import get_pr_files, post_comment
from services.ai_service import analyze_code
from services.db_service import save_review
from utils.logger import logger


async def handle_webhook(data: dict):
    action = data.get("action")
    repository = data.get("repository", {})
    pr = data.get("pull_request", {})
    repo = repository.get("full_name")
    pr_number = pr.get("number")
    pr_title = pr.get("title", "")

    logger.info(f"Webhook received: action={action}, repo={repo}, PR={pr_number}")

    if action not in ["opened", "synchronize", "reopened"]:
        logger.info(f"Action '{action}' ignored, only processing 'opened/synchronize/reopened'")
        return {"msg": "ignored"}

    if not repo or not pr_number:
        logger.error("Invalid webhook payload: missing repo or PR number")
        return {"msg": "invalid payload"}

    try:
        logger.info(f"Fetching PR files for {repo}#{pr_number}")
        files = await get_pr_files(repo, pr_number)
        diff = "\n".join([file.get("patch", "") for file in files if file.get("patch")])

        logger.info(f"Analyzing code diff ({len(diff)} chars)")
        review = await analyze_code(diff)

        logger.info(f"Saving review to database for {repo}#{pr_number}")
        db_review = {
            "title": pr_title,
            "repository": repo,
            "pr_number": pr_number,
            "status": "completed",
            "summary": review.get("summary", ""),
            "issues": review.get("issues", []),
            "suggestions": review.get("suggestions", []),
            "payload": data,
        }
        await save_review(db_review)

        logger.info(f"Posting comment to PR {repo}#{pr_number}")
        await post_comment(repo, pr_number, review)

        logger.info(f"Review complete for {repo}#{pr_number}")
        return {"msg": "review done", "review": review}

    except Exception as exc:
        logger.error(f"Error processing webhook: {str(exc)}", exc_info=True)
        raise
