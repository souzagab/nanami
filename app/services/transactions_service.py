from datetime import date, datetime
from typing import List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from ynab.models.new_transaction import NewTransaction as YNABTransaction

from app.models.account_mapping import AccountMapping
from app.models.transaction import Transaction
from app.models.types.enums import AccountMappingType
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.pluggy import PluggyTransaction
from app.services.account_mapping_service import AccountMappingService
from app.services.pluggy_service import PluggyService
from app.services.ynab_service import YNABService


class TransactionsService:
  def __init__(self, session: AsyncSession):
    self._ynab_service = YNABService()
    self._pluggy_service = PluggyService()
    self._account_mapping_service = AccountMappingService(session)
    self._transaction_repository = TransactionRepository(session)

  async def get_transactions(
    self, account_mapping_id: UUID, page: int = 1, page_size: int = 20
  ) -> tuple[List[Transaction], int, int, int]:
    """
    Retrieves transactions for a given account_mapping_id with pagination details.

    Returns:
        A tuple containing (transactions, total_items, total_pages, current_page).
    """
    if page < 1:
      page = 1
    if page_size < 1:
      page_size = 20  # Default page size

    skip = (page - 1) * page_size
    transactions, total_items = await self._transaction_repository.get_by_account_id_paginated(
      account_mapping_id=account_mapping_id, skip=skip, limit=page_size
    )

    total_pages = (total_items + page_size - 1) // page_size

    return transactions, total_items, total_pages, page

  async def sync_transactions(self, account_id: UUID):
    """
    Syncs transactions for a specific account
    """
    account = await self._find_account(account_id)

    if not account:
      raise ValueError(f"Account mapping {account_id} not found")

    await self._store_transactions(account)
    await self._process_transactions(account)

  async def _find_account(self, account_mapping_id: UUID) -> AccountMapping | None:
    return await self._account_mapping_service.find_account(account_mapping_id)

  async def _store_transactions(self, account: AccountMapping):
    latest_sync_date = await self._transaction_repository.get_latest_synced_transaction_date(account.id)
    if latest_sync_date:
      from_date_for_pluggy = latest_sync_date
    else:
      from_date_for_pluggy = date.today()

    pluggy_transactions: List[PluggyTransaction] = await self._pluggy_service.get_transactions(
      account_id=account.pluggy_account_id,
      from_date=from_date_for_pluggy,
    )

    if pluggy_transactions:
      for pluggy_transaction in pluggy_transactions:
        # Ensure pluggy_transaction.date is naive UTC for storage
        # It comes in as aware UTC from Pluggy
        transaction_date_naive = pluggy_transaction.date.replace(tzinfo=None)

        transaction_amount = self._parse_ammount(account, pluggy_transaction.amount)

        new_transaction = Transaction(
          account_mapping_id=account.id,
          pluggy_transaction_id=pluggy_transaction.id,
          transaction_date=transaction_date_naive,
          amount=transaction_amount,
          description=pluggy_transaction.description,
          raw_transaction=pluggy_transaction.model_dump(mode="json"),
        )

        try:
          await self._transaction_repository.find_or_create(new_transaction)
        except Exception:
          # Log critical error if find_or_create fails beyond handled IntegrityError
          # For now, re-raise to trigger session rollback in the caller
          raise

  async def _process_transactions(self, account: AccountMapping):
    unsynced_transactions = await self._transaction_repository.get_unsynced_by_account_id(account.id)

    for transaction in unsynced_transactions:
      ynab_transaction_date = transaction.transaction_date.date()
      milliunits_amount = int(transaction.amount * 1000)

      ynab_payload = YNABTransaction(
        account_id=account.ynab_account_id,
        date=ynab_transaction_date,
        amount=milliunits_amount,
        memo=transaction.description,
        import_id=str(transaction.id),
      )

      try:
        ynab_transaction_response = self._ynab_service.create_transaction(ynab_payload)
        # Use naive UTC for synced_at, consistent with DB column type and BaseModel
        transaction.synced_at = datetime.utcnow()
        transaction.ynab_transaction_id = ynab_transaction_response.data.transaction.id
        await self._transaction_repository.update(transaction)
      except Exception:
        # Log error; transaction remains unsynced. Re-raise to trigger session rollback.
        raise

  def _parse_ammount(self, account: AccountMapping, amount: float):
    credit_types = [AccountMappingType.CREDIT_CARD]

    if account.account_type in credit_types:
      return -amount
    return amount
