from uuid import UUID

from pydantic import BaseModel

from app.models.types.enums import AccountMappingStatus, AccountMappingType


class AccountMappingBase(BaseModel):
  name: str
  account_type: AccountMappingType
  pluggy_item_id: str
  pluggy_account_id: str
  ynab_account_id: str
  status: AccountMappingStatus = AccountMappingStatus.ACTIVE


class AccountMappingCreate(AccountMappingBase):
  pass


class AccountMappingUpdate(BaseModel):
  name: str | None = None
  account_type: AccountMappingType | None = None
  pluggy_item_id: str | None = None
  pluggy_account_id: str | None = None
  ynab_account_id: str | None = None
  status: AccountMappingStatus | None = None


class AccountMappingRead(AccountMappingBase):
  id: UUID
  ynab_budget_id: str

  class Config:
    from_attributes = True
