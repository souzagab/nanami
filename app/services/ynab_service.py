from ynab.models.new_transaction import NewTransaction
from ynab.models.post_transactions_wrapper import PostTransactionsWrapper
from ynab.models.save_transactions_response import SaveTransactionsResponse

from app.clients.ynab_client import YNABClient


class YNABService:
  def __init__(self):
    self._client = YNABClient()

  def create_transaction(self, transaction: NewTransaction) -> SaveTransactionsResponse:
    payload = PostTransactionsWrapper(transaction=transaction)

    return self._client.create_transaction(payload)
