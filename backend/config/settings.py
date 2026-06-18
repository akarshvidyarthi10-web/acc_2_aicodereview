from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve env file from the backend folder (or repo root) so startup works
# regardless of the current working directory.
BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_CANDIDATES = [
    BACKEND_DIR / ".env",
    BACKEND_DIR.parent / ".env",
    Path.cwd() / ".env",
]

for env_path in ENV_CANDIDATES:
    if env_path.exists():
        load_dotenv(env_path, override=False)
        break


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    github_token: str | None = None
    # Gemini / Google generative AI settings
    gemini_api_key: str | None = None
    # Prefer a lower-quota model by default because the free-tier quota on
    # gemini-2.5-flash can exhaust quickly during multi-agent reviews.
    gemini_model: str | None = "gemini-1.5-flash"
    gemini_model_fallback: str | None = "gemini-1.5-flash"
    github_app_id: str | None = None
    github_webhook_secret: str | None = None
    mongodb_uri: str | None = None
    mongodb_db_name: str | None = None


settings = Settings()
