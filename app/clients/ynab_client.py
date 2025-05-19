from ynab import TransactionsApi
from ynab import YNABClient as YNABLibClient
from ynab.models.post_transactions_wrapper import PostTransactionsWrapper
from ynab.models.save_transactions_response import SaveTransactionsResponse
from ynab.rest import ApiException

from app.core.settings import settings


class YNABClient:
  def __init__(self):
    self._api_client = YNABLibClient(settings.ynab_access_token)
    self._budget_id = settings.ynab_default_budget

  def create_transaction(
    self,
    transaction: PostTransactionsWrapper,
  ) -> SaveTransactionsResponse:
    api_instance = TransactionsApi(self._api_client)
    target_budget_id = self._budget_id
    try:
      response = api_instance.create_transaction(
        target_budget_id,
        transaction,
      )
    except ApiException as e:
      raise e

    return response
