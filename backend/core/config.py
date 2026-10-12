"""Central application configuration, loaded from environment / .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    env: str = "development"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/turfturtule"


settings = Settings()
