from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  logging_level: str = Field(default="INFO", alias="LOG_LEVEL")

  project_name: str = "Nanami"

  database_url: str = "postgresql+asyncpg://postgres:secret@localhost:5432/nanami"

  model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
