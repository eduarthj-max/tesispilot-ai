from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/tesispilot"
    OPENAI_API_KEY: str | None = None
    PROJECT_NAME: str = "TesisPilot"

    # Auth
    SECRET_KEY: str = "supersecret_replace_in_prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"

settings = Settings()
