from fastapi import APIRouter, Request, HTTPException, Header
from controllers.webhook_controller import handle_webhook
from utils.github_webhook import verify_github_signature

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request, x_hub_signature_256: str | None = Header(None)):
    body = await request.body()
    verify_github_signature(x_hub_signature_256, body)

    try:
        data = await request.json()
        return await handle_webhook(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
