from datetime import datetime
from typing import Optional

from libs.pluggy.models.transaction import GetTransactionResponse, ListTransactionsResponse
from libs.pluggy.session_manager import SessionManager


class TransactionClient:
  """
  Client for interacting with the Transaction endpoints of the Pluggy API.
  """

  def __init__(self, session: SessionManager):
    """
    Initializes the TransactionClient.

    Args:
        session (SessionManager): An instance of SessionManager.
    """
    self.session = session

  def list_transactions(
    self,
    account_id: str,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page_size: Optional[int] = 20,
    page: Optional[int] = 1,
  ) -> ListTransactionsResponse:
    """
    Lists all transactions for a specific account.

    Args:
        account_id (str): Account primary identifier.
        from_date (datetime, optional): Filter transactions from this date (inclusive).
        to_date (datetime, optional): Filter transactions up to this date (inclusive).
        page_size (int, optional): Number of transactions per page.
        page (int, optional): Page number.

    Returns:
        ListTransactionsResponse: The response containing transactions and pagination details.

    Raises:
        httpx.HTTPStatusError: If the request fails.
    """
    url = "/transactions"
    params = {
      "accountId": account_id,
      "pageSize": page_size,
      "page": page,
    }
    if from_date:
      params["from"] = from_date.strftime("%Y-%m-%d")
    if to_date:
      params["to"] = to_date.strftime("%Y-%m-%d")

    response = self.session.request_sync("GET", url, params=params)
    return ListTransactionsResponse(**response)

  async def async_list_transactions(
    self,
    account_id: str,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page_size: Optional[int] = 20,
    page: Optional[int] = 1,
  ) -> ListTransactionsResponse:
    """
    Asynchronously lists all transactions for a specific account.

    Args:
        account_id (str): Account primary identifier.
        from_date (datetime, optional): Filter transactions from this date (inclusive).
        to_date (datetime, optional): Filter transactions up to this date (inclusive).
        page_size (int, optional): Number of transactions per page.
        page (int, optional): Page number.

    Returns:
        ListTransactionsResponse: The response containing transactions and pagination details.

    Raises:
        httpx.HTTPStatusError: If the request fails.
    """
    url = "/transactions"
    params = {
      "accountId": account_id,
      "pageSize": page_size,
      "page": page,
    }
    if from_date:
      params["from"] = from_date.strftime("%Y-%m-%d")
    if to_date:
      params["to"] = to_date.strftime("%Y-%m-%d")

    response = await self.session.request_async("GET", url, params=params)
    return ListTransactionsResponse(**response)

  def get_transaction(self, transaction_id: str) -> GetTransactionResponse:
    """
    Retrieves a specific transaction by its ID.

    Args:
        transaction_id (str): The ID of the transaction to retrieve.

    Returns:
        GetTransactionResponse: The retrieved transaction details.

    Raises:
        httpx.HTTPStatusError: If the request fails.
    """
    url = f"/transactions/{transaction_id}"
    response = self.session.request_sync("GET", url)
    return GetTransactionResponse(**response)

  async def async_get_transaction(self, transaction_id: str) -> GetTransactionResponse:
    """
    Asynchronously retrieves a specific transaction by its ID.

    Args:
        transaction_id (str): The ID of the transaction to retrieve.

    Returns:
        GetTransactionResponse: The retrieved transaction details.

    Raises:
        httpx.HTTPStatusError: If the request fails.
    """
    url = f"/transactions/{transaction_id}"
    response = await self.session.request_async("GET", url)
    return GetTransactionResponse(**response)
