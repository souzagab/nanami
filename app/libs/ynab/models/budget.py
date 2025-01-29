from datetime import date
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .account import Account
    from .category import Category, CategoryGroup
    from .payee import Payee, PayeeLocation
    from .transaction import (
        MonthDetail,
        ScheduledSubTransaction,
        ScheduledTransactionDetail,
        SubTransaction,
        TransactionDetail,
    )


class BudgetSummary(BaseModel):
  """
  Represents a summary of a budget.
  """

  id: UUID = Field(..., description="The unique identifier of the budget")
  name: str = Field(..., description="The name of the budget")
  last_modified_on: Optional[str] = Field(None, description="The last time any changes were made to the budget")
  first_month: date = Field(..., description="The earliest budget month")
  last_month: date = Field(..., description="The latest budget month")
  date_format: dict = Field(..., description="The date format setting for the budget")
  currency_format: dict = Field(..., description="The currency format setting for the budget")
  accounts: Optional[List["Account"]] = Field(None, description="The list of budget accounts (if requested)")  # type: ignore


class BudgetDetail(BaseModel):
  """
  Represents detailed information about a budget.
  """

  id: UUID = Field(..., description="The unique identifier of the budget")
  name: str = Field(..., description="The name of the budget")
  last_modified_on: Optional[str] = Field(None, description="The last time any changes were made to the budget")
  date_format: dict = Field(..., description="The date format setting for the budget")
  currency_format: dict = Field(..., description="The currency format setting for the budget")
  accounts: List["Account"] = Field(..., description="The list of budget accounts")  # type: ignore
  payees: List["Payee"] = Field(..., description="The list of payees")  # type: ignore
  payee_locations: List["PayeeLocation"] = Field(..., description="The list of payee locations")  # type: ignore
  category_groups: List["CategoryGroup"] = Field(..., description="The list of category groups")  # type: ignore
  categories: List["Category"] = Field(..., description="The list of categories")  # type: ignore
  months: List["MonthDetail"] = Field(..., description="The list of months")  # type: ignore
  transactions: List["TransactionDetail"] = Field(..., description="The list of transactions")  # type: ignore
  subtransactions: List["SubTransaction"] = Field(..., description="The list of subtransactions")  # type: ignore
  scheduled_transactions: List["ScheduledTransactionDetail"] = Field(
    ..., description="The list of scheduled transactions"
  )  # type: ignore
  scheduled_subtransactions: List["ScheduledSubTransaction"] = Field(
    ..., description="The list of scheduled subtransactions"
  )  # type: ignore


class BudgetSettings(BaseModel):
  """
  Represents the settings of a budget.
  """

  date_format: dict = Field(..., description="The date format setting for the budget")
  currency_format: dict = Field(..., description="The currency format setting for the budget")


class BudgetsResponseData(BaseModel):
  budgets: List[BudgetSummary]
  default_budget: Optional[BudgetSummary]


class BudgetsResponse(BaseModel):
  data: BudgetsResponseData


class BudgetResponseData(BaseModel):
  budget: BudgetDetail
  server_knowledge: int


class BudgetResponse(BaseModel):
  data: BudgetResponseData


class BudgetSettingsResponseData(BaseModel):
  settings: BudgetSettings


class BudgetSettingsResponse(BaseModel):
  data: BudgetSettingsResponseData
