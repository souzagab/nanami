from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    project_name: str = "Nanami API"
    version: str = "0.1.0"
    description: str = "Middleman between OpenFinance and YNAB"

    # YNAB Configuration
    ynab_access_token: str
    ynab_async_mode: bool = True

    # Pluggy Configuration
    pluggy_client_id: str
    pluggy_client_secret: str
    pluggy_async_mode: bool = True

    # Database Configuration
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/nanami"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
