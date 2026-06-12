import os
import httpx
from config.settings import settings

GITHUB_API_URL = "https://api.github.com"


async def get_pr_files(repo: str, pr_number: int):
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def post_comment(repo: str, pr_number: int, review: dict):
    url = f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
    }
    body = {
        "body": review.get("comment", "AI review result is ready.")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
