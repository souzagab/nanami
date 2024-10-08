from typing import Optional

import httpx

from app.config.settings import Settings

from .clients.accounts_client import AccountsClient
from .clients.budgets_client import BudgetsClient
from .clients.transactions_client import TransactionsClient


class YNABClient:
  """
  The main client for interacting with the YNAB API.
  """

  BASE_URL = "https://api.youneedabudget.com/v1"

  def __init__(self, access_token: Optional[str] = None, async_mode: Optional[bool] = False):
    """
    Initializes the YNABClient with the provided access token.

    Args:
        access_token (str): Your personal access token for the YNAB API.
        async_mode (bool): If True, uses an asynchronous HTTP client.
    """
    self.access_token = access_token or Settings.ynab_access_token
    self.async_mode = async_mode or Settings.ynab_async_mode

    if not self.access_token:
      raise ValueError("YNAB_ACCESS_TOKEN must be provided either as arguments or environment variables.")

    self.headers = {
      "Authorization": f"Bearer {self.access_token}",
      "Accept": "application/json",
    }

    self.async_mode = async_mode

    if self.async_mode:
      self.session = httpx.AsyncClient(headers=self.headers, base_url=self.BASE_URL)
    else:
      self.session = httpx.Client(headers=self.headers, base_url=self.BASE_URL)

    # API Contexts
    self.budgets = BudgetsClient(self.session, async_mode=self.async_mode)
    self.accounts = AccountsClient(self.session, async_mode=self.async_mode)
    self.transactions = TransactionsClient(self.session, async_mode=self.async_mode)

  def close(self):
    """
    Closes the HTTP session.
    """
    self.session.close()

  async def aclose(self):
    """
    Asynchronously closes the HTTP session.
    """
    await self.session.aclose()
