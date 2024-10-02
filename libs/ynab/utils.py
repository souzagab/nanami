import httpx
from exceptions import BadRequestError, NotFoundError, YNABError
from pydantic import ValidationError


def parse_response(response, model):
  try:
    response.raise_for_status()
    json_data = response.json()
    return model.parse_obj(json_data).data
  except httpx.HTTPStatusError as e:
    status_code = e.response.status_code
    if status_code == 404:
      raise NotFoundError("Resource not found", response=e.response)
    elif status_code == 400:
      raise BadRequestError("Bad request", response=e.response)
    else:
      raise YNABError(f"HTTP error {status_code}", response=e.response)
  except ValidationError as e:
    raise YNABError(f"Data validation error: {e}", response=response)
