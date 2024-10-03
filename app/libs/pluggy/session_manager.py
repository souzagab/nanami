import time
from typing import Any, Dict, Optional

import httpx

from config.settings import Settings

from .models.auth import AuthRequest, AuthResponse


class SessionManager:
    """
    A client that handles session management, authentication, headers, and error handling.
    """

    BASE_URL = "https://api.pluggy.ai"

    def __init__(
            self,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            async_mode: bool = False,
    ):
        """
        Initializes a Session with client credentials.

        Args:
            client_id (str, optional): Pluggy API client ID.
            client_secret (str, optional): Pluggy API client secret.
            async_mode (bool): If True, uses an asynchronous HTTP client.
        """
        self.client_id = client_id or Settings.pluggy_client_id
        self.client_secret = client_secret or Settings.pluggy_client_secret
        self.async_mode = async_mode

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "PLUGGY_CLIENT_ID and PLUGGY_CLIENT_SECRET must be provided either as arguments or environment variables."
            )

        self.api_key: Optional[str] = None
        self.api_key_expires_at: float = 0

        if self.async_mode:
            self.session = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={"Content-Type": "application/json"},
            )
        else:
            self.session = httpx.Client(
                base_url=self.BASE_URL,
                headers={"Content-Type": "application/json"},
            )

    def close(self):
        """
        Closes the synchronous HTTP session.
        """
        if not self.async_mode:
            self.session.close()

    async def async_close(self):
        """
        Asynchronously closes the HTTP session.
        """
        if self.async_mode:
            await self.session.aclose()

    def authenticate(self):
        """
        Authenticates with the Pluggy API to obtain an API key.
        """
        auth_url = "/auth"
        auth_payload = AuthRequest(
            clientId=self.client_id, clientSecret=self.client_secret
        ).model_dump()

        response = self.session.post(auth_url, json=auth_payload)
        if response.status_code == 200:
            auth_response = AuthResponse(**response.json())
            self.api_key = auth_response.apiKey

            # Set expiration time based on API specifications (e.g., 24 hours)
            self.api_key_expires_at = time.time() + 24 * 60 * 60
        else:
            self.handle_error(response)

    async def async_authenticate(self):
        """
        Asynchronously authenticates with the Pluggy API to obtain an API key.
        """
        auth_url = "/auth"
        auth_payload = AuthRequest(
            clientId=self.client_id, clientSecret=self.client_secret
        ).model_dump()

        response = await self.session.post(auth_url, json=auth_payload)
        if response.status_code == 200:
            auth_response = AuthResponse(**response.json())
            self.api_key = auth_response.apiKey
            self.api_key_expires_at = time.time() + 24 * 60 * 60
        else:
            await self.async_handle_error(response)

    def get_api_key(self) -> str:
        """
        Retrieves the API key, refreshing it if necessary.

        Returns:
            str: The API key.
        """
        if not self.api_key or time.time() > self.api_key_expires_at:
            self.authenticate()
        return self.api_key

    async def async_get_api_key(self) -> str:
        """
        Asynchronously retrieves the API key, refreshing it if necessary.

        Returns:
            str: The API key.
        """
        if not self.api_key or time.time() > self.api_key_expires_at:
            await self.async_authenticate()
        return self.api_key

    def get_headers(self) -> Dict[str, str]:
        """
        Constructs headers for authenticated requests.

        Returns:
            dict: Headers including the API key.
        """
        return {
            "Content-Type": "application/json",
            "X-API-KEY": self.get_api_key(),
        }

    async def async_get_headers(self) -> Dict[str, str]:
        """
        Asynchronously constructs headers for authenticated requests.

        Returns:
            dict: Headers including the API key.
        """
        return {
            "Content-Type": "application/json",
            "X-API-KEY": await self.async_get_api_key(),
        }

    def handle_error(self, response: httpx.Response):
        """
        Handles HTTP errors by raising appropriate exceptions.

        Args:
            response (httpx.Response): The HTTP response.

        Raises:
            httpx.HTTPStatusError: If the response contains an HTTP error status.
        """
        raise httpx.HTTPStatusError(
            f"Request failed with status code {response.status_code}: {response.text}",
            request=response.request,
            response=response,
        )

    async def async_handle_error(self, response: httpx.Response):
        """
        Asynchronously handles HTTP errors by raising appropriate exceptions.

        Args:
            response (httpx.Response): The HTTP response.

        Raises:
            httpx.HTTPStatusError: If the response contains an HTTP error status.
        """
        raise httpx.HTTPStatusError(
            f"Request failed with status code {response.status_code}: {response.text}",
            request=response.request,
            response=response,
        )

    def request_sync(
            self,
            method: str,
            url: str,
            **kwargs: Any,
    ) -> Any:
        """
        A generic method to make HTTP requests synchronously.

        Args:
            method (str): HTTP method (GET, POST, etc.).
            url (str): Endpoint URL.
            **kwargs: Additional arguments for the request.

        Returns:
            Any: The parsed JSON response.

        Raises:
            httpx.HTTPStatusError: If the response contains an HTTP error status.
        """
        headers = self.get_headers()
        response = self.session.request(method, url, headers=headers, **kwargs)
        if response.status_code >= 400:
            self.handle_error(response)
        return response.json()

    async def request_async(
            self,
            method: str,
            url: str,
            **kwargs: Any,
    ) -> Any:
        """
        A generic method to make HTTP requests asynchronously.

        Args:
            method (str): HTTP method (GET, POST, etc.).
            url (str): Endpoint URL.
            **kwargs: Additional arguments for the request.

        Returns:
            Any: The parsed JSON response.

        Raises:
            httpx.HTTPStatusError: If the response contains an HTTP error status.
        """
        headers = await self.async_get_headers()
        response = await self.session.request(method, url, headers=headers, **kwargs)
        if response.status_code >= 400:
            await self.async_handle_error(response)
        return response.json()
