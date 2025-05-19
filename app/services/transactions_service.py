from datetime import datetime
from typing import List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from ynab.models.new_transaction import NewTransaction as YNABTransaction

from app.models.account_mapping import AccountMapping
from app.schemas.pluggy import PluggyTransaction
from app.services.account_mapping_service import AccountMappingService
from app.services.pluggy_service import PluggyService
from app.services.ynab_service import YNABService


class TransactionsService:
  def __init__(self, session: AsyncSession):
    self._ynab_service = YNABService()
    self._pluggy_service = PluggyService()
    self._account_mapping_service = AccountMappingService(session)

  async def sync_transactions(self, account_id: UUID):
    """
    Syncs transactions for a specific account
    """
    account = await self._find_account(account_id)

    if not account:
      raise ValueError(f"Account {account_id} not found")

    from_date = datetime.now().date()

    transactions: List[PluggyTransaction] = await self._pluggy_service.get_transactions(
      account_id=account.pluggy_account_id,
      from_date=from_date,
    )

    for transaction_data in transactions:
      transaction_date = transaction_data.date
      if isinstance(transaction_date, datetime):
        transaction_date = transaction_date.date()

      milliunits_amount = int(transaction_data.amount * 1000)

      ynab_transaction = YNABTransaction(
        account_id=account.ynab_account_id,
        date=transaction_date,
        amount=milliunits_amount,
        memo=transaction_data.description,
      )

      self._ynab_service.create_transaction(ynab_transaction)

  async def _find_account(self, account_id: UUID) -> AccountMapping | None:
    return await self._account_mapping_service.find_account(account_id)
