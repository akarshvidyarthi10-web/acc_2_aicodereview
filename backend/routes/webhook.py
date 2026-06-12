from fastapi import APIRouter, Request, HTTPException
from controllers.webhook_controller import handle_webhook

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    try:
        return await handle_webhook(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
