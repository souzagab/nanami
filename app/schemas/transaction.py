import datetime
from uuid import UUID

from pydantic import BaseModel


class TransactionRead(BaseModel):
  id: UUID
  transaction_date: datetime.datetime
  amount: float
  description: str | None
  synced_at: datetime.datetime | None

  class Config:
    from_attributes = True


class PaginatedTransactionResponse(BaseModel):
  items: list[TransactionRead]
  total_items: int
  total_pages: int
  page: int
