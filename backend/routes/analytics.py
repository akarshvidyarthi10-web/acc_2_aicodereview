"""
Analytics routes for dashboard, charts, and statistics
"""
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import List, Dict, Any
from services.db_service import get_database

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def _security_issues(review: dict) -> list:
    return review.get("security_issues") or review.get("security") or []


def _code_smells(review: dict) -> list:
    return review.get("code_smells") or review.get("smells") or []


def _naming_issues(review: dict) -> list:
    return review.get("naming_issues") or review.get("naming") or []


def _best_practices(review: dict) -> list:
    return review.get("best_practice_suggestions") or review.get("suggestions") or []


@router.get("/dashboard")
async def get_dashboard(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get dashboard statistics and KPIs
    Returns: PRs reviewed, critical issues, average score, repositories, success rate, avg response time
    """
    try:
        reviews = db.reviews

        all_reviews = await reviews.find({}).to_list(None)
        total_prs = len(all_reviews)

        critical_count = 0
        total_smells = 0
        repo_counts = {}

        scores = [r.get("review_score", 50) for r in all_reviews]
        successful = len([s for s in scores if s > 70])

        for review in all_reviews:
            security_issues = _security_issues(review)
            for issue in security_issues:
                if issue.get("severity") == "HIGH":
                    critical_count += 1

            smells = _code_smells(review)
            total_smells += len(smells)

            repo = review.get("repository") or review.get("repo_full_name")
            if repo:
                repo_counts[repo] = repo_counts.get(repo, 0) + 1

        avg_score = sum(scores) / len(scores) if scores else 0
        avg_response_time = 0
        processing_times = [r.get("processing_time", 0) for r in all_reviews]
        if processing_times:
            clean_times = []
            for value in processing_times:
                if isinstance(value, (int, float)):
                    clean_times.append(value)
                elif isinstance(value, str) and value.endswith('s'):
                    try:
                        clean_times.append(float(value[:-1]))
                    except ValueError:
                        pass
            avg_response_time = sum(clean_times) / len(clean_times) if clean_times else 0

        top_repo = None
        if repo_counts:
            top_repo = max(repo_counts.items(), key=lambda kv: kv[1])[0]

        return {
            "total_prs": total_prs,
            "critical_issues": critical_count,
            "average_score": round(avg_score, 1),
            "total_repos": len(repo_counts),
            "success_rate": round((successful / len(scores) * 100) if scores else 0, 1),
            "avg_time": round(avg_response_time, 2),
            "pr_trend": 0,
            "critical_trend": 0,
            "score_trend": 0,
            "avg_smells": round((total_smells / len(all_reviews)) if all_reviews else 0, 1),
            "top_repo": top_repo or "N/A",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard: {str(e)}")


@router.get("/charts")
async def get_charts(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get chart data for analytics
    """
    try:
        reviews = db.reviews
        all_reviews = await reviews.find({}).to_list(None)

        high_count = 0
        medium_count = 0
        low_count = 0
        security_count = 0
        smell_count = 0
        naming_count = 0
        practice_count = 0
        scores = []

        for review in all_reviews:
            for issue in _security_issues(review):
                security_count += 1
                severity = issue.get("severity", "LOW")
                if severity == "HIGH":
                    high_count += 1
                elif severity == "MEDIUM":
                    medium_count += 1
                else:
                    low_count += 1

            for issue in _code_smells(review):
                smell_count += 1
                severity = issue.get("severity", "LOW")
                if severity == "HIGH":
                    high_count += 1
                elif severity == "MEDIUM":
                    medium_count += 1
                else:
                    low_count += 1

            naming_count += len(_naming_issues(review))
            practice_count += len(_best_practices(review))
            scores.append(review.get("review_score", 50))

        return {
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count,
            "security_count": security_count,
            "smell_count": smell_count,
            "naming_count": naming_count,
            "practice_count": practice_count,
            "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "score_distribution": {
                "0-20": len([s for s in scores if s < 20]),
                "20-40": len([s for s in scores if 20 <= s < 40]),
                "40-60": len([s for s in scores if 40 <= s < 60]),
                "60-80": len([s for s in scores if 60 <= s < 80]),
                "80-100": len([s for s in scores if s >= 80]),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching charts: {str(e)}")


@router.get("/timeline-stats")
async def get_timeline_stats(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get timeline statistics (reviews over time)
    """
    try:
        reviews = db.reviews
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        daily_reviews = {}
        for i in range(30):
            date = (datetime.utcnow() - timedelta(days=29-i)).date()
            daily_reviews[str(date)] = 0

        all_reviews = await reviews.find({}).to_list(None)
        for review in all_reviews:
            created_at = review.get("created_at", datetime.utcnow())
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

            if created_at >= thirty_days_ago:
                date_str = created_at.date()
                if str(date_str) in daily_reviews:
                    daily_reviews[str(date_str)] += 1

        return {"daily_reviews": daily_reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching timeline: {str(e)}")
