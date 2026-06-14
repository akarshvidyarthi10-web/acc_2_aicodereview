import uuid
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

mongo_uri = settings.mongodb_uri or "mongodb://localhost:27017"
client = AsyncIOMotorClient(mongo_uri)
db = client.ai_code_review


async def list_reviews():
    cursor = db.reviews.find().sort("created_at", -1)
    return [review async for review in cursor]


async def get_review_by_id(review_id: str):
    return await db.reviews.find_one({"id": review_id})


async def save_review(review: dict):
    review.setdefault("id", str(uuid.uuid4()))
    review.setdefault("created_at", datetime.utcnow().isoformat() + "Z")
    await db.reviews.insert_one(review)
    return review
