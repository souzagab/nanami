from datetime import datetime
from typing import Optional

import httpx

from ..models.transaction import GetTransactionResponse, ListTransactionsResponse


class TransactionClient:
    """Client for Pluggy Transaction endpoints."""

    def __init__(self, client: httpx.Client | httpx.AsyncClient) -> None:
        """Initialize the transactions client.
        
        Args:
            client: HTTP client instance
        """
        self._client = client

    async def list_transactions(
        self,
        account_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page_size: int = 20,
        page: int = 1,
    ) -> ListTransactionsResponse:
        """List transactions for an account.
        
        Args:
            account_id: Account ID to get transactions for
            from_date: Filter from date
            to_date: Filter to date
            page_size: Number of results per page
            page: Page number
            
        Returns:
            List of transactions with pagination
        """
        params = {
            "accountId": account_id,
            "pageSize": page_size,
            "page": page,
        }
        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")

        response = await self._client.get("/transactions", params=params)
        response.raise_for_status()
        return ListTransactionsResponse(**response.json())

    async def get_transaction(self, transaction_id: str) -> GetTransactionResponse:
        """Get a single transaction.
        
        Args:
            transaction_id: ID of transaction to get
            
        Returns:
            Transaction details
        """
        response = await self._client.get(f"/transactions/{transaction_id}")
        response.raise_for_status()
        return GetTransactionResponse(**response.json())
