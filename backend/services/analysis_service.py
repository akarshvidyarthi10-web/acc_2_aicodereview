from typing import List
from services.db_service import list_reviews, get_review_by_id, save_review


async def fetch_review_list() -> List[dict]:
    return await list_reviews()


async def fetch_review_details(review_id: str) -> dict:
    review = await get_review_by_id(review_id)
    if review:
        return review
    return {
        "id": review_id,
        "title": "Manual review stub",
        "status": "pending",
        "summary": "Details will be available after review.",
        "issues": [],
        "suggestions": [],
    }


async def execute_manual_review(payload: dict) -> dict:
    review = {
        "title": payload.get("title", "Manual review request"),
        "status": "queued",
        "summary": "Review request received and queued.",
        "issues": [],
        "suggestions": [],
        "payload": payload,
    }
    await save_review(review)
    return review
