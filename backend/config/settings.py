import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    github_token: str | None = None
    bedrock_model: str | None = None
    bedrock_region: str | None = None
    github_app_id: str | None = None
    github_webhook_secret: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
