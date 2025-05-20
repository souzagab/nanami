import math
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.models.account_mapping import AccountMapping
from app.models.transaction import Transaction
from app.services.account_mapping_service import AccountMappingService
from app.services.transactions_service import TransactionsService

router = APIRouter(prefix="/accounts/{account_mapping_id}/transactions", tags=["transactions"])
templates = Jinja2Templates(directory="app/templates")


def get_transactions_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> TransactionsService:
  return TransactionsService(session)


def get_account_mapping_service(
  session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AccountMappingService:
  return AccountMappingService(session)


@router.get("", response_class=HTMLResponse, name="list_transactions_for_account")
async def list_transactions_for_account(
  request: Request,
  account_mapping_id: UUID,
  page: int = Query(1, ge=1),
  page_size: int = Query(20, ge=1, le=100),
  account_mapping_service: AccountMappingService = Depends(get_account_mapping_service),
  transactions_service: TransactionsService = Depends(get_transactions_service),
):
  account_mapping: AccountMapping | None = await account_mapping_service.find_account(account_mapping_id)
  if not account_mapping:
    raise HTTPException(status_code=404, detail="Account mapping not found")

  transactions_data: tuple[list[Transaction], int, int, int] = await transactions_service.get_transactions(
    account_mapping_id=account_mapping_id, page=page, page_size=page_size
  )
  transactions, total_items, total_pages, current_page = transactions_data

  return templates.TemplateResponse(
    "transactions/list.html",
    {
      "request": request,
      "account_mapping": account_mapping,
      "transactions": transactions,
      "total_items": total_items,
      "total_pages": total_pages,
      "current_page": current_page,
      "page_size": page_size,
      "math": math,  # Pass math for template calculations if needed (e.g. range for pagination)
    },
  )


@router.post("/sync", name="sync_account_transactions")
async def sync_account_transactions_endpoint(
  request: Request,
  account_mapping_id: UUID,  # This comes from the router's prefix
  transactions_service: TransactionsService = Depends(get_transactions_service),
):
  """
  Triggers synchronization of transactions for a specific account mapping.
  """
  try:
    # The service method sync_transactions expects account_id, which is our account_mapping_id
    await transactions_service.sync_transactions(account_id=account_mapping_id)
    # Redirect back to the account mappings list page
    redirect_url = request.app.url_path_for("list_account_mappings")
    return RedirectResponse(url=redirect_url, status_code=303)
  except ValueError as e:
    # If account mapping not found or other value error during sync
    raise HTTPException(status_code=404, detail=str(e))
  except Exception:
    # Catch any other unexpected errors during the sync process
    # Log this e ideally
    raise HTTPException(status_code=500, detail="An unexpected error occurred during transaction synchronization.")
