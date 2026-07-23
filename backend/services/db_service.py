import uuid
from datetime import datetime
from urllib.parse import urlparse
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

mongo_uri = settings.mongodb_uri or "mongodb://localhost:27017"
client = AsyncIOMotorClient(mongo_uri)

# Use explicit DB name if configured, otherwise infer from URI path or fallback.
if settings.mongodb_db_name:
    db_name = settings.mongodb_db_name
else:
    parsed = urlparse(mongo_uri)
    db_name = parsed.path.lstrip('/') or 'ai_code_review'

if not db_name:
    db_name = 'ai_code_review'

print(f"Using MongoDB database: {db_name}")
db = client[db_name]


def serialize_review(review: dict | None) -> dict | None:
    if not review:
        return review

    review = dict(review)
    if review.get("_id") is not None:
        review["_id"] = str(review["_id"])
    if isinstance(review.get("created_at"), datetime):
        review["created_at"] = review["created_at"].isoformat() + "Z"
    return review


async def list_reviews():
    cursor = db.reviews.find().sort("created_at", -1)
    return [serialize_review(review) async for review in cursor]


async def get_review_by_id(review_id: str):
    review = await db.reviews.find_one({"id": review_id})
    if not review and ObjectId.is_valid(review_id):
        review = await db.reviews.find_one({"_id": ObjectId(review_id)})
    return serialize_review(review)


async def save_review(review: dict):
    review.setdefault("id", str(uuid.uuid4()))
    review.setdefault("created_at", datetime.utcnow().isoformat() + "Z")
    result = await db.reviews.insert_one(review)
    review["_id"] = str(result.inserted_id)
    return review


def get_database():
    return db
