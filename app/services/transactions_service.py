from datetime import datetime, timedelta
from typing import List

from ynab.models.new_transaction import NewTransaction as YNABTransaction

from app.schemas.pluggy import PluggyTransaction
from app.services.pluggy_service import PluggyService
from app.services.ynab_service import YNABService


class TransactionsService:
  def __init__(self):
    self._ynab_service = YNABService()
    self._pluggy_service = PluggyService()

  async def sync_transactions(self, account_id: str):
    transactions: List[PluggyTransaction] = await self._pluggy_service.get_transactions(
      account_id,
      start_date=datetime.now() - timedelta(days=1),
    )

    for transaction in transactions:
      ynab_transaction = YNABTransaction(
        date=transaction.date,
        amount=transaction.amount,
      )

      await self._ynab_service.create_transaction(ynab_transaction)
