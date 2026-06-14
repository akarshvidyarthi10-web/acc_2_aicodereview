import hmac
import hashlib

from fastapi import Header, HTTPException
from config.settings import settings


def verify_github_signature(signature: str | None, payload_body: bytes) -> None:
    if not settings.github_webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret is not configured.")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing GitHub signature header.")

    if not signature.startswith("sha256="):
        raise HTTPException(status_code=400, detail="Unsupported signature format.")

    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        payload_body,
        hashlib.sha256,
    ).hexdigest()
    provided = signature.split("=", 1)[1]

    if not hmac.compare_digest(expected, provided):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature.")
