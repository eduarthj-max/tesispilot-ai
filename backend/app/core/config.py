from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/tesispilot"
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    PROJECT_NAME: str = "TesisPilot"

    # Zotero integration
    ZOTERO_API_URL: str = "https://api.zotero.org"
    ZOTERO_API_KEY: str | None = None
    ZOTERO_USER_ID: str | None = None
    ZOTERO_LIBRARY_TYPE: str = "user"
    ZOTERO_DEFAULT_COLLECTION_ID: str | None = None

    # Auth
    SECRET_KEY: str = "supersecret_replace_in_prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"


settings = Settings()
