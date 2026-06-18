import asyncio
from services.db_service import save_review, list_reviews, get_review_by_id

async def test_mongo():
    review = {
        "title": "Mongo Test Review",
        "repository": "test/repo",
        "pr_number": 999,
        "status": "completed",
        "summary": "This is a test review.",
        "security": [],
        "smells": [],
        "naming": [],
        "suggestions": ["Mongo connection successful."],
        "review_score": 100,
        "model": "gemini-2.5-flash",
        "processing_time": "0.01s",
        "review_version": "v1",
    }

    saved = await save_review(review)
    print('Saved review id:', saved['id'])

    found = await get_review_by_id(saved['id'])
    print('Found review summary:', found['summary'])

    all_reviews = await list_reviews()
    print('Total reviews:', len(all_reviews))

if __name__ == '__main__':
    asyncio.run(test_mongo())
