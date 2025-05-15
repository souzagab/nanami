from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AccountType(str, Enum):
  CHECKING = "checking"
  SAVINGS = "savings"
  CASH = "cash"
  CREDIT_CARD = "creditCard"
  LINE_OF_CREDIT = "lineOfCredit"
  OTHER_ASSET = "otherAsset"
  OTHER_LIABILITY = "otherLiability"
  MORTGAGE = "mortgage"
  AUTO_LOAN = "autoLoan"
  STUDENT_LOAN = "studentLoan"
  PERSONAL_LOAN = "personalLoan"
  MEDICAL_DEBT = "medicalDebt"
  OTHER_DEBT = "otherDebt"


class Account(BaseModel):
  """
  Represents a YNAB account.
  """

  id: UUID = Field(..., description="The unique identifier of the account")
  name: str = Field(..., description="The name of the account")
  type: AccountType = Field(..., description="The type of account")
  on_budget: bool = Field(..., description="Whether the account is on budget")
  closed: bool = Field(..., description="Whether the account is closed")
  note: Optional[str] = Field(None, description="Notes about the account")
  balance: int = Field(..., description="Current balance in milliunits")
  cleared_balance: int = Field(..., description="Cleared balance in milliunits")
  uncleared_balance: int = Field(..., description="Uncleared balance in milliunits")
  transfer_payee_id: Optional[UUID] = Field(None, description="The payee ID for transfers to this account")
  deleted: bool = Field(..., description="Whether the account is deleted")

  direct_import_linked: Optional[bool] = Field(
    None,
    description="Whether the account is linked for direct import",
  )
  direct_import_in_error: Optional[bool] = Field(
    None,
    description="Whether the linked direct import is in error",
  )
  last_reconciled_at: Optional[str] = Field(
    None,
    description="ISO 8601 formatted date of the last reconciliation",
  )
  debt_original_balance: Optional[int] = Field(
    None,
    description="The original balance for debt accounts in milliunits",
  )
  debt_interest_rates: Optional[Dict[str, int]] = Field(
    None,
    description="Interest rates for debt accounts",
  )
  debt_minimum_payments: Optional[Dict[str, int]] = Field(
    None,
    description="Minimum payments for debt accounts",
  )
  debt_escrow_amounts: Optional[Dict[str, int]] = Field(
    None,
    description="Escrow amounts for debt accounts",
  )


class CreateAccount(BaseModel):
  """
  Represents the data required to create a new account.
  """

  name: str = Field(..., description="The name of the account")
  type: AccountType = Field(..., description="The type of account")
  balance: int = Field(..., description="Initial balance in milliunits")
  note: Optional[str] = Field(None, description="Notes about the account")
  on_budget: Optional[bool] = Field(True, description="Whether the account is on budget")
  closed: Optional[bool] = Field(False, description="Whether the account is closed")


class AccountData(BaseModel):
  account: Account


class AccountResponse(BaseModel):
  data: AccountData


class AccountsData(BaseModel):
  accounts: List[Account]
  server_knowledge: int


class AccountsResponse(BaseModel):
  data: AccountsData
