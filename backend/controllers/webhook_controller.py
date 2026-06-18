import json
import traceback

from config.settings import settings
from services.ai_service import analyze_code
from services.db_service import save_review
from services.github_service import (
    get_pr_files,
    post_comment,
    post_review_with_inline_comments,
)
from utils.logger import logger


async def handle_webhook(data: dict):
    action = data.get("action")
    repository = data.get("repository", {})
    pr = data.get("pull_request", {})
    repo = repository.get("full_name")
    pr_number = pr.get("number")
    pr_title = pr.get("title", "")
    commit_sha = pr.get("head", {}).get("sha")

    logger.info(
        "Webhook stage=received action=%s repo=%s pr=%s commit=%s",
        action,
        repo,
        pr_number,
        commit_sha,
    )

    if action not in ["opened", "synchronize", "reopened"]:
        logger.info(
            "Webhook stage=filter action=%s skipped_reason=unsupported_action",
            action,
        )
        return {"msg": "ignored"}

    if not repo or not pr_number:
        logger.error(
            "Webhook stage=validation repo=%s pr=%s error=missing_repo_or_pr",
            repo,
            pr_number,
        )
        return {"msg": "invalid payload"}

    try:
        logger.info(
            "Webhook stage=fetch_pr_files repo=%s pr=%s started",
            repo,
            pr_number,
        )
        files = await get_pr_files(repo, pr_number)
        logger.info(
            "Webhook stage=fetch_pr_files repo=%s pr=%s status=success file_count=%s",
            repo,
            pr_number,
            len(files),
        )

        diff_with_files = []
        for file in files:
            filename = file.get("filename", "")
            patch = file.get("patch", "")
            if patch:
                diff_with_files.append(f"--- a/{filename}\n+++ b/{filename}\n{patch}")

        diff = "\n".join(diff_with_files)
        logger.info(
            "Webhook stage=diff_build repo=%s pr=%s diff_chars=%s file_count=%s",
            repo,
            pr_number,
            len(diff),
            len(files),
        )

        logger.info(
            "Webhook stage=analyze_code repo=%s pr=%s started",
            repo,
            pr_number,
        )
        review = await analyze_code(diff)
        logger.info(
            "Webhook stage=analyze_code repo=%s pr=%s completed review_score=%s",
            repo,
            pr_number,
            review.get("review_score", 0),
        )

        try:
            logger.info("Final review payload=%s", json.dumps(review, indent=2, default=str))
        except Exception:
            logger.info("Final review payload raw=%s", review)

        for issue_list in [review.get("security", []), review.get("smells", []), review.get("naming", [])]:
            for issue in issue_list:
                if not issue.get("file") and files:
                    issue["file"] = files[0].get("filename", "")
                if not issue.get("line"):
                    issue["line"] = 1

        logger.info(
            "Webhook stage=save_review repo=%s pr=%s started",
            repo,
            pr_number,
        )
        db_review = {
            "title": pr_title,
            "repository": repo,
            "pr_number": pr_number,
            "status": "completed",
            "summary": review.get("summary", ""),
            "security": review.get("security", []),
            "smells": review.get("smells", []),
            "naming": review.get("naming", []),
            "suggestions": review.get("suggestions", []),
            "review_score": review.get("review_score", 0),
            "model": review.get("model", settings.gemini_model or "gemini-2.5-flash"),
            "processing_time": review.get("processing_time", ""),
            "review_version": review.get("review_version", "v2-langgraph"),
            "payload": data,
        }
        await save_review(db_review)
        logger.info(
            "Webhook stage=save_review repo=%s pr=%s completed review_id=%s",
            repo,
            pr_number,
            db_review.get("id"),
        )

        logger.info(
            "Webhook stage=post_comment repo=%s pr=%s commit=%s started",
            repo,
            pr_number,
            commit_sha,
        )
        try:
            if commit_sha:
                response = await post_review_with_inline_comments(repo, pr_number, review, commit_sha)
                logger.info(
                    "Webhook stage=post_comment repo=%s pr=%s response=%s",
                    repo,
                    pr_number,
                    response,
                )
            else:
                logger.warning(
                    "Webhook stage=post_comment repo=%s pr=%s reason=no_commit_sha fallback_to_regular_comment",
                    repo,
                    pr_number,
                )
                response = await post_comment(repo, pr_number, review)
                logger.info(
                    "Webhook stage=post_comment repo=%s pr=%s response=%s",
                    repo,
                    pr_number,
                    response,
                )
        except Exception as comment_error:
            logger.exception(
                "Webhook stage=post_comment repo=%s pr=%s error=%s",
                repo,
                pr_number,
                comment_error,
            )
            response = await post_comment(repo, pr_number, review)
            logger.info(
                "Webhook stage=post_comment repo=%s pr=%s fallback_response=%s",
                repo,
                pr_number,
                response,
            )

        logger.info(
            "Webhook stage=complete repo=%s pr=%s summary_length=%s",
            repo,
            pr_number,
            len(review.get("summary", "")),
        )
        return {"msg": "review done", "review": review}

    except Exception as exc:
        logger.exception(
            "Webhook stage=error repo=%s pr=%s error=%s",
            repo,
            pr_number,
            exc,
        )
        raise
