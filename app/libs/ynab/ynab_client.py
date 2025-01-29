from typing import Optional

from app.config.settings import settings
from app.libs.base_client import BaseAPIClient

from .clients.accounts_client import AccountsClient
from .clients.budgets_client import BudgetsClient
from .clients.transactions_client import TransactionsClient


class YNABClient(BaseAPIClient):
    """Client for interacting with the YNAB API."""

    BASE_URL = "https://api.youneedabudget.com/v1"

    def __init__(
        self,
        access_token: Optional[str] = None,
        async_mode: bool = True,
    ) -> None:
        """Initialize the YNAB client.
        
        Args:
            access_token: YNAB API access token
            async_mode: Whether to use async client
        """
        self.access_token = access_token or settings.ynab_access_token
        if not self.access_token:
            raise ValueError("YNAB access token is required")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

        super().__init__(
            base_url=self.BASE_URL,
            headers=headers,
            async_mode=async_mode,
        )

        # Initialize API clients
        self.budgets = BudgetsClient(self._client)
        self.accounts = AccountsClient(self._client)
        self.transactions = TransactionsClient(self._client)
