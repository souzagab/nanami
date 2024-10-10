from typing import Optional

from .clients.items_client import ItemsClient
from .clients.transactions_client import TransactionClient
from .session_manager import SessionManager


class PluggyAIClient:
  """
  The main client for interacting with the Pluggy API.
  """

  def __init__(
    self,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    async_mode: bool = False,
  ):
    """
    Initializes the PluggyAIClient with client credentials and a list of item IDs.

    Args:
        client_id (str, optional): Pluggy API client ID.
        client_secret (str, optional): Pluggy API client secret.
        async_mode (bool): If True, uses an asynchronous HTTP client.
    """
    self.session = SessionManager(
      client_id=client_id,
      client_secret=client_secret,
      async_mode=async_mode,
    )

    self.items = ItemsClient(self.session)
    self.transactions = TransactionClient(self.session)

  def close(self):
    """
    Closes the synchronous HTTP session.
    """
    self.session.close()

  async def async_close(self):
    """
    Asynchronously closes the HTTP session.
    """
    await self.session.async_close()
