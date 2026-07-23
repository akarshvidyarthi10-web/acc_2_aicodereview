import asyncio
import json
import traceback

from fastapi import APIRouter, Request, HTTPException, Header
from controllers.webhook_controller import handle_webhook
from utils.github_webhook import verify_github_signature
from utils.logger import logger

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request, x_hub_signature_256: str | None = Header(None)):
    body = await request.body()
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    delivery_id = request.headers.get("X-GitHub-Delivery", "unknown")

    logger.info(
        "Webhook received: event=%s delivery=%s content_length=%s",
        event_type,
        delivery_id,
        len(body),
    )

    try:
        verify_github_signature(x_hub_signature_256, body)
        logger.info("Webhook signature verification: OK")
    except Exception as exc:
        logger.exception("Webhook signature verification failed: %s", exc)
        raise HTTPException(status_code=401, detail=str(exc))

    try:
        data = json.loads(body)
        action = data.get("action")
        repo = data.get("repository", {}).get("full_name", "unknown")
        pr = data.get("pull_request", {})
        pr_number = pr.get("number")
        logger.info(
            "Webhook payload parsed: event=%s action=%s repo=%s pr=%s",
            event_type,
            action,
            repo,
            pr_number,
        )

        # Return 200 immediately so GitHub sees delivery success while processing continues.
        asyncio.create_task(handle_webhook(data))
        return {
            "status": "accepted",
            "event": event_type,
            "action": action,
            "repository": repo,
            "pull_request": pr_number,
        }
    except Exception as exc:
        logger.exception("Webhook payload processing failed")
        raise HTTPException(status_code=500, detail=str(exc))
