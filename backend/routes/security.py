from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.db_service import get_database

router = APIRouter(prefix="/api/security", tags=["security"])


def _security_issues(review: dict) -> list:
    return review.get("security_issues") or review.get("security") or []


def _repo_name(review: dict) -> str:
    return review.get("repository") or review.get("repo_full_name") or "Unknown"


@router.get("/issues")
async def get_security_issues(
    severity: str | None = Query(None, description="Filter by issue severity"),
    repository: str | None = Query(None, description="Filter by repository name"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    reviews = await db.reviews.find({}).to_list(None)
    issues = []

    for review in reviews:
        repo_name = _repo_name(review)
        for issue in _security_issues(review):
            if severity and issue.get("severity") != severity:
                continue
            if repository and repo_name != repository:
                continue

            issues.append(
                {
                    **issue,
                    "repository": repo_name,
                    "pr_number": review.get("pr_number"),
                    "created_at": review.get("created_at"),
                }
            )

    return {"issues": issues}
