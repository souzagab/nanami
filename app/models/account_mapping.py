from sqlmodel import Field

from app.core import settings
from app.models.base import BaseModel
from app.models.types.enums import AccountMappingStatus, AccountMappingType


class AccountMapping(BaseModel, table=True):
  # Model for mapping Pluggy accounts to YNAB accounts to sync transactions
  __tablename__ = "account_mappings"

  name: str = Field(index=True, description="User-defined name for this mapping")

  account_type: AccountMappingType = Field(description="User-defined type for this account")
  status: AccountMappingStatus = Field(default=AccountMappingStatus.ACTIVE, description="Status of the mapping")

  pluggy_item_id: str = Field(index=True, description="Pluggy Item ID (manual user input)")
  pluggy_account_id: str = Field(index=True, unique=True, description="Specific Account ID from Pluggy")

  ynab_account_id: str = Field(index=True, description="Account ID from YNAB")
  ynab_budget_id: str = Field(default=settings.ynab_default_budget, description="Budget ID from YNAB")
