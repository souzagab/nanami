from datetime import date
from typing import List

from app.clients.pluggy_client import PluggyClient
from app.schemas.pluggy import PluggyTransaction, PluggyTransactionsRequestParams


class PluggyService:
  def __init__(self):
    self._client = PluggyClient()

  async def get_transactions(self, account_id: str, from_date: date) -> List[PluggyTransaction]:
    params = PluggyTransactionsRequestParams(
      from_date=from_date,
    )

    response = self._client.list_transactions(
      account_id,
      params,
    )

    return response.results
