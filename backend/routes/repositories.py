"""
Repositories routes for repository health and stats
"""
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.db_service import get_database

router = APIRouter(prefix="/api/repositories", tags=["repositories"])


def _security_issues(review: dict) -> list:
    return review.get("security_issues") or review.get("security") or []


def _code_smells(review: dict) -> list:
    return review.get("code_smells") or review.get("smells") or []


@router.get("")
async def get_repositories(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get all repositories with health metrics
    """
    try:
        reviews = db.reviews
        all_reviews = await reviews.find({}).to_list(None)

        repos = {}
        for review in all_reviews:
            repo_name = review.get("repository") or review.get("repo_full_name") or "Unknown"
            if repo_name not in repos:
                repos[repo_name] = {
                    "name": repo_name,
                    "total_reviews": 0,
                    "average_score": 0,
                    "critical_issues": 0,
                    "high_issues": 0,
                    "medium_issues": 0,
                    "low_issues": 0,
                    "last_review": None,
                    "scores": [],
                }

            repos[repo_name]["total_reviews"] += 1
            score = review.get("review_score", 50)
            repos[repo_name]["scores"].append(score)

            for issue in _security_issues(review):
                severity = issue.get("severity", "LOW")
                if severity == "HIGH":
                    repos[repo_name]["critical_issues"] += 1
                elif severity == "MEDIUM":
                    repos[repo_name]["high_issues"] += 1
                else:
                    repos[repo_name]["medium_issues"] += 1

            for issue in _code_smells(review):
                severity = issue.get("severity", "LOW")
                if severity == "HIGH":
                    repos[repo_name]["critical_issues"] += 1
                elif severity == "MEDIUM":
                    repos[repo_name]["high_issues"] += 1
                else:
                    repos[repo_name]["medium_issues"] += 1

            if review.get("created_at"):
                repos[repo_name]["last_review"] = review.get("created_at")

        result = []
        for repo_name, data in repos.items():
            if data["scores"]:
                data["average_score"] = round(sum(data["scores"]) / len(data["scores"]), 1)
            del data["scores"]
            result.append(data)

        return {"repositories": sorted(result, key=lambda x: x["average_score"], reverse=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repositories: {str(e)}")


@router.get("/{repo_name}")
async def get_repository_detail(repo_name: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get detailed stats for a specific repository
    """
    try:
        reviews = db.reviews
        repo_reviews = await reviews.find({"repository": repo_name}).to_list(None)

        if not repo_reviews:
            raise HTTPException(status_code=404, detail=f"Repository '{repo_name}' not found")

        scores = [r.get("review_score", 50) for r in repo_reviews]
        total_issues = 0
        high_severity = 0

        for review in repo_reviews:
            total_issues += len(_security_issues(review))
            total_issues += len(_code_smells(review))
            high_severity += len([i for i in _security_issues(review) if i.get("severity") == "HIGH"])

        return {
            "repository": repo_name,
            "total_reviews": len(repo_reviews),
            "average_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "total_issues_found": total_issues,
            "high_severity_issues": high_severity,
            "health_percentage": round((sum(scores) / len(scores)) if scores else 0),
            "recent_reviews": [
                {
                    "pr_number": r.get("pr_number"),
                    "score": r.get("review_score"),
                    "created_at": r.get("created_at"),
                }
                for r in sorted(repo_reviews, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repository detail: {str(e)}")
