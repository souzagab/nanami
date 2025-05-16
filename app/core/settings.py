from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
  PROJECT_NAME: str = "Nanami"

  DATABASE_URL: str = "postgresql+asyncpg://postgres:secret@localhost:5432/nanami"

  model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
