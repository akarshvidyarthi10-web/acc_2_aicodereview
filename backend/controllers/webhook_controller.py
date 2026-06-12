from services.github_service import get_pr_files, post_comment
from services.ai_service import analyze_code


async def handle_webhook(data: dict):
    if data.get("action") != "opened":
        return {"msg": "ignored"}

    repository = data.get("repository", {})
    pr = data.get("pull_request", {})
    repo = repository.get("full_name")
    pr_number = pr.get("number")

    if not repo or not pr_number:
        return {"msg": "invalid payload"}

    files = await get_pr_files(repo, pr_number)
    diff = "\n".join([file.get("patch", "") for file in files if file.get("patch")])
    review = await analyze_code(diff)
    await post_comment(repo, pr_number, review)

    return {"msg": "review done", "review": review}
