from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  logging_level: str = Field(default="INFO", alias="LOG_LEVEL")

  project_name: str = "Nanami"

  database_url: str = "postgresql+asyncpg://postgres:secret@localhost:5432/nanami"

  ynab_api_url: str = Field(default="https://api.ynab.com/v1")
  ynab_default_budget: str
  ynab_access_token: str

  pluggy_api_url: str = Field(default="https://api.pluggy.ai")
  pluggy_client_id: str
  pluggy_client_secret: str

  model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
