# app/ynab_sdk/utils.py

import httpx
from libs.ynab.exceptions import BudgetNotFoundError, TransactionNotFoundError, YNABClientError
from pydantic import ValidationError


def parse_response(response: httpx.Response, model):
  """
  Parses and validates the HTTP response using the provided Pydantic model.

  Args:
      response (httpx.Response): The HTTP response object.
      model (BaseModel): The Pydantic model to parse the response data.

  Returns:
      Parsed data as per the Pydantic model.

  Raises:
      BudgetNotFoundError: If a 404 status code is returned for budgets.
      TransactionNotFoundError: If a 404 status code is returned for transactions.
      YNABClientError: For other HTTP errors or validation issues.
  """
  try:
    response.raise_for_status()
    json_data = response.json()
    return model.parse_obj(json_data).data
  except httpx.HTTPStatusError as e:
    status_code = e.response.status_code
    if status_code == 404:
      # Determine if it's a budget or transaction based on URL or content
      url = e.request.url.path
      if "/budgets/" in url and "/transactions/" in url:
        transaction_id = url.split("/")[-1]
        raise TransactionNotFoundError(transaction_id=transaction_id) from e
      else:
        budget_id = url.split("/")[-1] if url.split("/")[-1] != "budgets" else "unknown"
        raise BudgetNotFoundError(budget_id=budget_id) from e
    elif status_code == 400:
      raise YNABClientError("Bad request.") from e
    else:
      raise YNABClientError(f"HTTP error {status_code}.") from e
  except ValidationError as e:
    raise YNABClientError(f"Data validation error: {e}") from e
