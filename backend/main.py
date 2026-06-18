from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import analytics, repositories, review, security, webhook
from config.settings import settings

app = FastAPI(
    title="AI Code Review Agent",
    description="GitHub PR code review using AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router, prefix="/api")
app.include_router(review.router, prefix="/api")
app.include_router(security.router, prefix="/api")
app.include_router(analytics.router)
app.include_router(repositories.router)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "AI Code Review Agent",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "webhook": "ok",
        "github": "ok" if settings.github_token else "missing",
        "gemini": "ok" if settings.gemini_api_key else "missing",
        "database": "ok" if settings.mongodb_uri else "missing",
    }
