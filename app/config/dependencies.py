from typing import AsyncGenerator

from fastapi import Request
from app.libs.pluggy.pluggy_client import PluggyAIClient
from app.libs.ynab.ynab_client import YNABClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import async_session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

def get_ynab_client(request: Request) -> YNABClient:
    """
    Dependency to retrieve the YNABClient from the application state.
    """
    return request.app.state.ynab_client

def get_pluggy_client(request: Request) -> PluggyAIClient:
    return request.app.state.pluggy_client

