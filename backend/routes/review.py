from fastapi import APIRouter, HTTPException
from controllers.review_controller import (
    get_reviews,
    get_review,
    get_review_timeline,
    get_review_agents,
    trigger_review,
)

router = APIRouter()

@router.get("/reviews")
async def list_reviews():
    return await get_reviews()

@router.get("/reviews/{review_id}")
async def review_details(review_id: str):
    return await get_review(review_id)

@router.get("/reviews/{review_id}/timeline")
async def review_timeline(review_id: str):
    return await get_review_timeline(review_id)

@router.get("/reviews/{review_id}/agents")
async def review_agents(review_id: str):
    return await get_review_agents(review_id)

@router.post("/reviews/run")
async def run_review(payload: dict):
    try:
        return await trigger_review(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
