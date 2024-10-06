import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
