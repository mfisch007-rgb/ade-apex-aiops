from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    ADE-APEX Global Configuration
    """

    APP_NAME: str = "ADE-APEX AI Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/ade_apex"
    )

    REDIS_URL: str = "redis://localhost:6379/0"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env.example",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
