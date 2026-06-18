import os
import httpx
from config.settings import settings

if not settings.github_token:
    raise SystemExit("GITHUB_TOKEN is not set in the environment.")

repo_owner = os.environ.get("TEST_GITHUB_REPO_OWNER")
repo_name = os.environ.get("TEST_GITHUB_REPO_NAME")
if not repo_owner or not repo_name:
    raise SystemExit("Set TEST_GITHUB_REPO_OWNER and TEST_GITHUB_REPO_NAME for GitHub API tests.")

url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
headers = {
    "Authorization": f"Bearer {settings.github_token}",
    "Accept": "application/vnd.github+json",
}

print('Querying repository:', url)
with httpx.Client() as client:
    response = client.get(url, headers=headers)
    response.raise_for_status()
    print('Repo response:')
    print(response.json())

files_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/1/files"
print('Querying PR files for PR #1:', files_url)
with httpx.Client() as client:
    response = client.get(files_url, headers=headers)
    if response.status_code == 404:
        print('PR #1 not found or no access to PR files yet. Response status:', response.status_code)
    else:
        response.raise_for_status()
        print('PR files response:')
        print(response.json())
