"""Typed application settings — single source of truth for configuration.

Loaded once from .env (pydantic-settings maps DATABASE_URL -> database_url).
Required values fail here, at startup, with a readable error — not
mysteriously at the first request.
"""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # unrelated vars in .env must not kill boot
        hide_input_in_errors=True,  # validation errors never echo secret values
    )

    env: str = "development"
    debug: bool = False  # safe polarity: production defaults quiet
    database_url: SecretStr  # required — no default; contains credentials


@lru_cache
def get_settings() -> Settings:
    return Settings()
