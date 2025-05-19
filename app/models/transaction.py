import datetime
from typing import Any, Dict
from uuid import UUID

from sqlmodel import JSON, Column, Field, UniqueConstraint

from app.models.base import BaseModel


class Transaction(BaseModel, table=True):
  __tablename__ = "transactions"

  account_mapping_id: UUID = Field(foreign_key="account_mappings.id", index=True)

  # Pluggy related fields
  pluggy_transaction_id: UUID = Field(index=True)

  # YNAB related fields
  ynab_transaction_id: str | None = Field(default=None, index=True)

  # Common transaction details
  transaction_date: datetime.datetime
  amount: float
  description: str | None = Field(default=None)

  # Sync timestamp
  synced_at: datetime.datetime | None = Field(
    default=None, index=True, description="The timestamp when the transaction was synced to YNAB"
  )

  raw_transaction: Dict[str, Any] | None = Field(
    default=None, sa_column=Column(JSON), description="The raw transaction data from Pluggy"
  )
  __table_args__ = (
    UniqueConstraint("account_mapping_id", "pluggy_transaction_id", name="uq_account_pluggy_transaction"),
    UniqueConstraint("account_mapping_id", "ynab_transaction_id", name="uq_account_ynab_transaction"),
  )
