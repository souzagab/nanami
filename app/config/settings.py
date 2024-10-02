import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    ynab_access_token: str = os.getenv("YNAB_ACCESS_TOKEN")
    ynab_async_mode: bool = os.getenv("YNAB_ASYNC_MODE", False)
    debug: bool = os.getenv("DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()