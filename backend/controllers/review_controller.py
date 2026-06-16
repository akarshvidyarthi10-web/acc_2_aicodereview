from services.analysis_service import fetch_review_list, fetch_review_details, execute_manual_review


async def get_reviews():
    return await fetch_review_list()


async def get_review review_id: str
    return await fetch_review_details(review_id)


async def trigger_review(payload: dict):
    return await execute_manual_review(payload)
