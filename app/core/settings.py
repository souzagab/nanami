from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  logging_level: str = Field(default="INFO", alias="LOG_LEVEL")

  project_name: str = "Nanami"

  database_url: str = "postgresql+asyncpg://postgres:secret@localhost:5432/nanami"

  ynab_default_budget: str
  ynab_access_token: str
  pluggy_client_id: str
  pluggy_client_secret: str

  model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
