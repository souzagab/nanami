from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.services.transactions_service import TransactionsService

router = APIRouter()


@router.get("/sync")
async def sync_all_transactions_endpoint(session: AsyncSession = Depends(get_async_session)):
  transactions_service = TransactionsService(session=session)
  await transactions_service.sync_all_transactions()
  return {"message": "Synchronization for all accounts initiated successfully"}
