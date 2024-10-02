from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

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
    last_modified_on: Optional[str] = Field(
        None, description="The last time any changes were made to the budget"
    )
    first_month: date = Field(..., description="The earliest budget month")
    last_month: date = Field(..., description="The latest budget month")
    date_format: dict = Field(..., description="The date format setting for the budget")
    currency_format: dict = Field(..., description="The currency format setting for the budget")
    accounts: Optional[List['Account']] = Field(
        None, description="The list of budget accounts (if requested)"
    )


class BudgetDetail(BaseModel):
    """
    Represents detailed information about a budget.
    """
    id: UUID = Field(..., description="The unique identifier of the budget")
    name: str = Field(..., description="The name of the budget")
    last_modified_on: Optional[str] = Field(
        None, description="The last time any changes were made to the budget"
    )
    date_format: dict = Field(..., description="The date format setting for the budget")
    currency_format: dict = Field(..., description="The currency format setting for the budget")
    accounts: List['Account'] = Field(..., description="The list of budget accounts")
    payees: List['Payee'] = Field(..., description="The list of payees")
    payee_locations: List['PayeeLocation'] = Field(..., description="The list of payee locations")
    category_groups: List['CategoryGroup'] = Field(..., description="The list of category groups")
    categories: List['Category'] = Field(..., description="The list of categories")
    months: List['MonthDetail'] = Field(..., description="The list of months")
    transactions: List['TransactionDetail'] = Field(..., description="The list of transactions")
    subtransactions: List['SubTransaction'] = Field(..., description="The list of subtransactions")
    scheduled_transactions: List['ScheduledTransactionDetail'] = Field(
        ..., description="The list of scheduled transactions"
    )
    scheduled_subtransactions: List['ScheduledSubTransaction'] = Field(
        ..., description="The list of scheduled subtransactions"
    )



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