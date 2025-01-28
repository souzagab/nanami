from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import async_session_maker
from app.libs.pluggy.pluggy_client import PluggyAIClient
from app.libs.ynab.ynab_client import YNABClient


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_ynab_client(request: Request) -> YNABClient:
    """Dependency that provides the YNAB client."""
    client = request.app.state.ynab_client
    return client


async def get_pluggy_client(request: Request) -> PluggyAIClient:
    """Dependency that provides the Pluggy client."""
    client = request.app.state.pluggy_client
    return client


# Common dependencies
DB = Annotated[AsyncSession, Depends(get_db)]
YNABClient = Annotated[YNABClient, Depends(get_ynab_client)]
PluggyClient = Annotated[PluggyAIClient, Depends(get_pluggy_client)]
