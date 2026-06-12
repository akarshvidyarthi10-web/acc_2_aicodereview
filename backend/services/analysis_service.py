from typing import List
from models.review_model import ReviewResult


async def fetch_review_list() -> List[dict]:
    # Placeholder: replace with persistent storage or database
    return []


async def fetch_review_details(review_id: str) -> dict:
    # Placeholder: return dummy object for now
    return {
        "id": review_id,
        "title": "Manual review stub",
        "status": "pending",
        "summary": "Details will be available after review.",
        "issues": [],
        "suggestions": [],
    }


async def execute_manual_review(payload: dict) -> dict:
    return {
        "status": "queued",
        "payload": payload,
        "message": "Manual review request received.",
    }
