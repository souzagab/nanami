from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Payee(BaseModel):
  """
  Represents a payee in a budget.
  """

  id: UUID = Field(..., description="The unique identifier of the payee")
  name: str = Field(..., description="The name of the payee")
  transfer_account_id: Optional[UUID] = Field(
    None, description="The account ID for transfers, if this is a transfer payee"
  )
  deleted: bool = Field(..., description="Whether the payee has been deleted")


class PayeeLocation(BaseModel):
  """
  Represents a payee location.
  """

  id: UUID = Field(..., description="The unique identifier of the payee location")
  payee_id: UUID = Field(..., description="The ID of the associated payee")
  latitude: str = Field(..., description="The latitude of the payee location")
  longitude: str = Field(..., description="The longitude of the payee location")
  deleted: bool = Field(..., description="Whether the payee location has been deleted")
