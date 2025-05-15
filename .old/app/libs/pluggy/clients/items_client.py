from ..models.item import Item
from ..session_manager import SessionManager


class ItemsClient:
  """
  Client for interacting with the Item endpoints of the Pluggy API.
  """

  def __init__(self, session: SessionManager):
    """
    Initializes the ItemClient.

    Args:
        session (SessionManager): An instance of BaseClient.
    """
    self.session = session

  def get_item(self, item_id: str) -> Item:
    """
    Retrieves a specific item by its ID.

    Args:
        item_id (str): The ID of the item to retrieve.

    Returns:
        Item: The retrieved item.

    Raises:
        httpx.HTTPStatusError: If the request fails.
    """
    url = f"/items/{item_id}"
    response = self.session.request_sync("GET", url)

    return Item(**response)

  async def async_get_item(self, item_id: str) -> Item:
    """
    Asynchronously retrieves a specific item by its ID.

    Args:
        item_id (str): The ID of the item to retrieve.

    Returns:
        Item: The retrieved item.

    Raises:
        httpx.HTTPStatusError: If the request fails.
    """
    url = f"/items/{item_id}"
    response = await self.session.request_async("GET", url)

    return Item(**response)
