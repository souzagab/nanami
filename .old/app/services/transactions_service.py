from app.libs import PluggyAIClient, YNABClient


class TransactionsService:
  def __init__(self, ynab_client: YNABClient, pluggy_client: PluggyAIClient):
    self.pluggy = pluggy_client
    self.ynab = ynab_client

  async def sync(self):
    pluggy_transactions = self.pluggy.transactions.list_transactions(account_id="987b4345-5fc2-4460-9b7c-6e3633b62410")
