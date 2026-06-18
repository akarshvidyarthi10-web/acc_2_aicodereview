from typing import List, Dict, Any
from services.analysis_service import fetch_review_list, fetch_review_details, execute_manual_review
from services.db_service import get_review_by_id


async def get_reviews() -> Dict[str, List[dict]]:
    return await fetch_review_list()


async def get_review(review_id: str) -> dict:
    return await fetch_review_details(review_id)


async def get_review_timeline(review_id: str) -> dict:
    review = await get_review_by_id(review_id)
    if not review:
        return {"events": []}

    events = [
        {
            "time": review.get("created_at"),
            "title": "Review created",
            "description": "The AI review was saved and is ready for inspection.",
        }
    ]

    if review.get("status"):
        events.append({
            "time": review.get("created_at"),
            "title": "Review status updated",
            "description": f"Status set to {review.get('status')}.",
        })

    return {"events": events}


async def get_review_agents(review_id: str) -> dict:
    review = await get_review_by_id(review_id)
    if not review:
        return {"agents": []}

    return {
        "agents": [
            {
                "name": "Security Agent",
                "status": "completed",
                "result_count": len(review.get("security", []) or []),
            },
            {
                "name": "Quality Agent",
                "status": "completed",
                "result_count": len(review.get("smells", []) or []) + len(review.get("naming", []) or []),
            },
            {
                "name": "Summary Agent",
                "status": "completed",
                "result_count": 1,
            },
        ]
    }


async def trigger_review(payload: dict) -> dict:
    return await execute_manual_review(payload)
