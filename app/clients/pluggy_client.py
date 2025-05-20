from uuid import UUID

import httpx

from app.core.settings import settings
from app.schemas.pluggy import PluggyTransactionsRequestParams, PluggyTransactionsResponse


class PluggyClient:
  def __init__(self):
    self._base_url = settings.pluggy_api_url

    self._api_key: str | None = None
    self._http_client = httpx.AsyncClient()

  async def list_transactions(
    self, account_id: UUID, query_params: PluggyTransactionsRequestParams
  ) -> PluggyTransactionsResponse:
    """
    Retrieves a list of transactions for a given account.
    """
    params_dict = query_params.model_dump(by_alias=True, exclude_none=True)
    params_dict["accountId"] = account_id

    response_data = await self._request(
      "GET",
      "/transactions",
      params=params_dict,
    )

    return PluggyTransactionsResponse(**response_data)

  async def _authenticate(self) -> None:
    """
    Authenticates with the Pluggy API and retrieves an API key.
    This method will always attempt to fetch a new key.
    """
    auth_url = f"{self._base_url}/auth"

    payload = {
      "clientId": settings.pluggy_client_id,
      "clientSecret": settings.pluggy_client_secret,
    }

    try:
      response = await self._http_client.post(auth_url, json=payload)
      response.raise_for_status()
      data = response.json()

      self._api_key = data["apiKey"]
    except httpx.HTTPStatusError as e:
      print(f"Authentication failed: {e.response.status_code} - {e.response.text}")
      raise
    except Exception as e:
      print(f"An unexpected error occurred during authentication: {e}")
      raise

  async def close(self):
    """
    Closes the underlying HTTP client.
    Should be called when the PluggyClient is no longer needed.
    """
    await self._http_client.aclose()

  async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
    """
    Makes an authenticated request to the Pluggy API.
    Handles API key management and retries on 401 errors by re-authenticating.
    """
    if not self._api_key:
      await self._authenticate()

    if not self._api_key:
      print("CRITICAL: API key is not available after initial authentication check.")
      raise Exception("API key could not be obtained or was not set by _authenticate.")

    current_api_key = self._api_key

    headers = kwargs.pop("headers", {})
    headers["X-API-KEY"] = current_api_key
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    url = f"{self._base_url}{endpoint}"

    try:
      response = await self._http_client.request(method, url, headers=headers, **kwargs)
      response.raise_for_status()
      if response.status_code == 204:  # No content
        return {}
      return response.json()
    except httpx.HTTPStatusError as e:
      if e.response.status_code == 401:
        print(
          f"Received 401 for {method} {endpoint}. API key might have expired or been revoked. Attempting to re-authenticate..."
        )

        await self._authenticate()

        if not self._api_key:
          print("CRITICAL: API key is not available after re-authentication attempt following 401.")
          raise Exception("API key could not be re-obtained after 401 or was not set by _authenticate.")

        headers["X-API-KEY"] = self._api_key

        print(f"Retrying {method} {endpoint} with new API key...")
        response = await self._http_client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        if response.status_code == 204:  # No content after retry
          return {}
        return response.json()
      else:
        print(f"HTTP error during request to {method} {endpoint}: {e.response.status_code} - {e.response.text}")
        raise  # Re-raise other HTTP errors
    except Exception as e:
      print(f"An unexpected error occurred during request to {method} {endpoint}: {e}")
      raise
