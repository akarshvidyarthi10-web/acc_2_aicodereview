from fastapi import APIRouter, HTTPException
from controllers.review_controller import get_reviews, get_review, trigger_review

router = APIRouter()

@router.get("/reviews")
async def list_reviews():
    return await get_reviews()

@router.get("/reviews/{review_id}")
async def review_details(review_id: str):
    return await get_review(review_id)

@router.post("/reviews/run")
async def run_review(payload: dict):
    try:
        return await trigger_review(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
