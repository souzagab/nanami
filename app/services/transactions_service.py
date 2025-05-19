from datetime import datetime, timedelta
from typing import List

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

  async def sync_all_transactions(self):
    accounts = await self._account_mapping_service.get_all_mappings()

    for account in accounts:
      await self._sync_transactions(account)

  async def _sync_transactions(self, account: AccountMapping):
    transactions: List[PluggyTransaction] = await self._pluggy_service.get_transactions(
      account_id=account.pluggy_account_id,
      from_date=(datetime.now() - timedelta(days=30)).date(),
    )

    for transaction in transactions:
      # Ensure transaction.date is a date object, not datetime
      transaction_date = transaction.date
      if isinstance(transaction_date, datetime):
        transaction_date = transaction_date.date()

      # Convert amount to milliunits (integer)
      # YNAB amounts are integers, e.g., $12.34 is 12340
      milliunits_amount = int(transaction.amount * 1000)

      ynab_transaction = YNABTransaction(
        account_id=account.ynab_account_id,
        date=transaction_date,
        amount=milliunits_amount,
        memo=transaction.description,
      )

      self._ynab_service.create_transaction(ynab_transaction)
