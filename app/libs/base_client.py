from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel


class BaseAPIClient:
    """Base class for API clients with common functionality."""
    
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        async_mode: bool = True,
    ):
        """Initialize the base client with common configuration."""
        self.base_url = base_url
        self.headers = headers or {}
        self.async_mode = async_mode
        
        # Initialize HTTP client
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
        ) if async_mode else httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
        )
    
    async def aclose(self) -> None:
        """Close async client."""
        if isinstance(self._client, httpx.AsyncClient):
            await self._client.aclose()
    
    def close(self) -> None:
        """Close sync client."""
        if isinstance(self._client, httpx.Client):
            self._client.close()
    
    async def _make_request(
        self,
        method: str,
        url: str,
        response_model: Optional[type[BaseModel]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make an HTTP request and handle the response."""
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode")
            
        response = await self._client.request(method, url, **kwargs)
        response.raise_for_status()
        
        if response_model:
            return response_model(**response.json())
        return response.json()
    
    def _make_request_sync(
        self,
        method: str,
        url: str,
        response_model: Optional[type[BaseModel]] = None,
        **kwargs: Any,
    ) -> Any:
        """Make a synchronous HTTP request and handle the response."""
        if self.async_mode:
            raise RuntimeError("Client is in async mode")
            
        response = self._client.request(method, url, **kwargs)
        response.raise_for_status()
        
        if response_model:
            return response_model(**response.json())
        return response.json()
