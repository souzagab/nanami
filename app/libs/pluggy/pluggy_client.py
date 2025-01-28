from typing import Optional

from app.config.settings import settings
from app.libs.base_client import BaseAPIClient

from .clients.items_client import ItemsClient
from .clients.transactions_client import TransactionClient


class PluggyClient(BaseAPIClient):
    """Client for interacting with the Pluggy API."""

    BASE_URL = "https://api.pluggy.ai"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        async_mode: bool = True,
    ) -> None:
        """Initialize the Pluggy client.
        
        Args:
            client_id: Pluggy API client ID
            client_secret: Pluggy API client secret
            async_mode: Whether to use async client
        """
        self.client_id = client_id or settings.pluggy_client_id
        self.client_secret = client_secret or settings.pluggy_client_secret

        if not self.client_id or not self.client_secret:
            raise ValueError("Pluggy client ID and secret are required")

        super().__init__(
            base_url=self.BASE_URL,
            async_mode=async_mode,
        )

        # Initialize API clients
        self.items = ItemsClient(self._client)
        self.transactions = TransactionClient(self._client)

    async def _get_auth_token(self) -> str:
        """Get authentication token."""
        response = await self._make_request(
            "POST",
            "/auth",
            json={
                "clientId": self.client_id,
                "clientSecret": self.client_secret,
            },
        )
        return response["apiKey"]

    async def authenticate(self) -> None:
        """Authenticate with Pluggy API."""
        token = await self._get_auth_token()
        self._client.headers["X-API-KEY"] = token
