import httpx

from libs.ynab.clients.accounts_client import AccountsClient


class YNABClient:
  """
  The main client for interacting with the YNAB API.
  """

  BASE_URL = "https://api.youneedabudget.com/v1"

  def __init__(self, access_token: str, async_mode: bool = False):
    """
    Initializes the YNABClient with the provided access token.

    Args:
        access_token (str): Your personal access token for the YNAB API.
        async_mode (bool): If True, uses an asynchronous HTTP client.
    """
    self.access_token = access_token
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
    self.accounts = AccountsClient(self.session, async_mode=self.async_mode)

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
