from fastapi import FastAPI
from routes import webhook, review

app = FastAPI(title="AI Code Review Agent")

app.include_router(webhook.router, prefix="/api")
app.include_router(review.router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok", "service": "AI Code Review Agent"}
