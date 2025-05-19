from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.services.transactions_service import TransactionsService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/sync/{mapping_id}", name="sync_single_account")
async def sync_single_account_transactions_endpoint(
  request: Request, mapping_id: UUID, session: AsyncSession = Depends(get_async_session)
):
  transactions_service = TransactionsService(session=session)
  try:
    await transactions_service.sync_transactions(mapping_id)
    redirect_url = request.app.url_path_for("list_account_mappings")
    return RedirectResponse(url=redirect_url, status_code=303)

  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
