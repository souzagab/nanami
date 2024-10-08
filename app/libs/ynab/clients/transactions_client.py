from typing import List, Optional

import httpx
from libs.ynab.models.transaction import (
  CreateTransaction,
  CreateTransactionResponse,
  Transaction,
  TransactionResponse,
  TransactionsResponse,
  UpdateTransaction,
  UpdateTransactionResponse,
)
from libs.ynab.utils import parse_response


class TransactionsClient:
  """
  API methods related to Transactions.
  """

  def __init__(self, client: httpx.Client, async_mode: bool = False):
    self.client = client
    self.async_mode = async_mode

  # --------------------
  # Asynchronous methods
  # --------------------

  async def get_transactions(
    self,
    budget_id: str,
    since_id: Optional[str] = None,
    last_knowledge_of_server: Optional[int] = None,
    include_subtransactions: bool = False,
  ) -> List[Transaction]:
    """
    Asynchronously retrieves a list of transactions for a given budget.

    Args:
        budget_id (str): The ID of the budget.
        since_id (Optional[str]): The ID of the last transaction that was retrieved.
        last_knowledge_of_server (Optional[int]): The knowledge of the server.
        include_subtransactions (bool): Whether to include subtransactions.

    Returns:
        List[Transaction]: A list of transactions.
    """
    if not self.async_mode:
      raise RuntimeError("Client is not in async mode; use 'get_transactions_sync' instead")

    params = {
      "since_id": since_id,
      "last_knowledge_of_server": last_knowledge_of_server,
      "include_subtransactions": str(include_subtransactions).lower(),
    }
    url = f"/budgets/{budget_id}/transactions"
    response = await self.client.get(url, params=params)
    data = parse_response(response, TransactionsResponse)
    return data.transactions

  async def get_transaction(self, budget_id: str, transaction_id: str) -> Transaction:
    """
    Asynchronously retrieves a single transaction by ID.

    Args:
        budget_id (str): The ID of the budget.
        transaction_id (str): The ID of the transaction.

    Returns:
        Transaction: The transaction details.
    """
    if not self.async_mode:
      raise RuntimeError("Client is not in async mode; use 'get_transaction_sync' instead")

    url = f"/budgets/{budget_id}/transactions/{transaction_id}"
    response = await self.client.get(url)
    data = parse_response(response, TransactionResponse)
    return data.transaction

  async def create_transaction(self, budget_id: str, transaction: CreateTransaction) -> Transaction:
    """
    Asynchronously creates a new transaction.

    Args:
        budget_id (str): The ID of the budget.
        transaction (CreateTransaction): The transaction data to create.

    Returns:
        Transaction: The created transaction.
    """
    if not self.async_mode:
      raise RuntimeError("Client is not in async mode; use 'create_transaction_sync' instead")

    url = f"/budgets/{budget_id}/transactions"
    payload = {"transaction": transaction.dict(exclude_unset=True)}
    response = await self.client.post(url, json=payload)
    data = parse_response(response, CreateTransactionResponse)
    return data.transaction

  async def update_transaction(
    self, budget_id: str, transaction_id: str, transaction: UpdateTransaction
  ) -> Transaction:
    """
    Asynchronously updates an existing transaction.

    Args:
        budget_id (str): The ID of the budget.
        transaction_id (str): The ID of the transaction.
        transaction (UpdateTransaction): The transaction data to update.

    Returns:
        Transaction: The updated transaction.
    """
    if not self.async_mode:
      raise RuntimeError("Client is not in async mode; use 'update_transaction_sync' instead")

    url = f"/budgets/{budget_id}/transactions/{transaction_id}"
    payload = {"transaction": transaction.dict(exclude_unset=True)}
    response = await self.client.patch(url, json=payload)
    data = parse_response(response, UpdateTransactionResponse)
    return data.transaction

  async def delete_transaction(self, budget_id: str, transaction_id: str) -> None:
    """
    Asynchronously deletes a transaction.

    Args:
        budget_id (str): The ID of the budget.
        transaction_id (str): The ID of the transaction.

    Returns:
        None
    """
    if not self.async_mode:
      raise RuntimeError("Client is not in async mode; use 'delete_transaction_sync' instead")

    url = f"/budgets/{budget_id}/transactions/{transaction_id}"
    response = await self.client.delete(url)
    parse_response(response, TransactionResponse)
    return

  # --------------------
  # Synchronous methods
  # --------------------

  def get_transactions_sync(
    self,
    budget_id: str,
    since_id: Optional[str] = None,
    last_knowledge_of_server: Optional[int] = None,
    include_subtransactions: bool = False,
  ) -> List[Transaction]:
    """
    Retrieves a list of transactions for a given budget.

    Args:
        budget_id (str): The ID of the budget.
        since_id (Optional[str]): The ID of the last transaction that was retrieved.
        last_knowledge_of_server (Optional[int]): The knowledge of the server.
        include_subtransactions (bool): Whether to include subtransactions.

    Returns:
        List[Transaction]: A list of transactions.
    """
    if self.async_mode:
      raise RuntimeError("Client is in async mode; use 'get_transactions' instead")

    params = {
      "since_id": since_id,
      "last_knowledge_of_server": last_knowledge_of_server,
      "include_subtransactions": str(include_subtransactions).lower(),
    }
    url = f"/budgets/{budget_id}/transactions"
    response = self.client.get(url, params=params)
    data = parse_response(response, TransactionsResponse)
    return data.transactions

  def get_transaction_sync(self, budget_id: str, transaction_id: str) -> Transaction:
    """
    Retrieves a single transaction by ID.

    Args:
        budget_id (str): The ID of the budget.
        transaction_id (str): The ID of the transaction.

    Returns:
        Transaction: The transaction details.
    """
    if self.async_mode:
      raise RuntimeError("Client is in async mode; use 'get_transaction' instead")

    url = f"/budgets/{budget_id}/transactions/{transaction_id}"
    response = self.client.get(url)
    data = parse_response(response, TransactionResponse)
    return data.transaction

  def create_transaction_sync(self, budget_id: str, transaction: CreateTransaction) -> Transaction:
    """
    Creates a new transaction.

    Args:
        budget_id (str): The ID of the budget.
        transaction (CreateTransaction): The transaction data to create.

    Returns:
        Transaction: The created transaction.
    """
    if self.async_mode:
      raise RuntimeError("Client is in async mode; use 'create_transaction' instead")

    url = f"/budgets/{budget_id}/transactions"
    payload = {"transaction": transaction.dict(exclude_unset=True)}
    response = self.client.post(url, json=payload)
    data = parse_response(response, CreateTransactionResponse)
    return data.transaction

  def update_transaction_sync(self, budget_id: str, transaction_id: str, transaction: UpdateTransaction) -> Transaction:
    """
    Updates an existing transaction.

    Args:
        budget_id (str): The ID of the budget.
        transaction_id (str): The ID of the transaction.
        transaction (UpdateTransaction): The transaction data to update.

    Returns:
        Transaction: The updated transaction.
    """
    if self.async_mode:
      raise RuntimeError("Client is in async mode; use 'update_transaction' instead")

    url = f"/budgets/{budget_id}/transactions/{transaction_id}"
    payload = {"transaction": transaction.dict(exclude_unset=True)}
    response = self.client.patch(url, json=payload)
    data = parse_response(response, UpdateTransactionResponse)
    return data.transaction

  def delete_transaction_sync(self, budget_id: str, transaction_id: str) -> None:
    """
    Deletes a transaction.

    Args:
        budget_id (str): The ID of the budget.
        transaction_id (str): The ID of the transaction.

    Returns:
        None
    """
    if self.async_mode:
      raise RuntimeError("Client is in async mode; use 'delete_transaction' instead")

    url = f"/budgets/{budget_id}/transactions/{transaction_id}"
    response = self.client.delete(url)
    parse_response(response, TransactionResponse)
    return
