from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/tesispilot"
    OPENAI_API_KEY: str | None = None
    PROJECT_NAME: str = "TesisPilot"

    class Config:
        env_file = ".env"

settings = Settings()
