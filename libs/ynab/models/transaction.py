from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .category import Category


class SubTransaction(BaseModel):
    """
    Represents a sub-transaction (part of a split transaction).
    """
    id: UUID = Field(..., description="The unique identifier of the sub-transaction")
    transaction_id: UUID = Field(..., description="The ID of the parent transaction")
    amount: int = Field(..., description="The amount of the sub-transaction in milliunits")
    memo: Optional[str] = Field(None, description="Memo associated with the sub-transaction")
    payee_id: Optional[UUID] = Field(None, description="The ID of the payee associated with the sub-transaction")
    category_id: Optional[UUID] = Field(None, description="The ID of the category associated with the sub-transaction")
    deleted: bool = Field(..., description="Whether the sub-transaction has been deleted")


class ScheduledTransactionDetail(BaseModel):
    """
    Represents a scheduled transaction.
    """
    id: UUID = Field(..., description="The unique identifier of the scheduled transaction")
    account_id: UUID = Field(..., description="The ID of the account associated with the scheduled transaction")
    date_first: date = Field(..., description="The first date the scheduled transaction is scheduled for")
    date_next: date = Field(..., description="The next date the scheduled transaction is scheduled for")
    frequency: str = Field(..., description="The frequency of the scheduled transaction")
    amount: int = Field(..., description="The amount of the scheduled transaction in milliunits")
    memo: Optional[str] = Field(None, description="Memo associated with the scheduled transaction")
    flag_color: Optional[str] = Field(None, description="Flag color of the scheduled transaction")
    deleted: bool = Field(..., description="Whether the scheduled transaction has been deleted")


class ScheduledSubTransaction(BaseModel):
    """
    Represents a scheduled sub-transaction (part of a scheduled split transaction).
    """
    id: UUID = Field(..., description="The unique identifier of the scheduled sub-transaction")
    scheduled_transaction_id: UUID = Field(..., description="The ID of the parent scheduled transaction")
    amount: int = Field(..., description="The amount of the scheduled sub-transaction in milliunits")
    memo: Optional[str] = Field(None, description="Memo associated with the scheduled sub-transaction")
    payee_id: Optional[UUID] = Field(None,
                                     description="The ID of the payee associated with the scheduled sub-transaction")
    category_id: Optional[UUID] = Field(None,
                                        description="The ID of the category associated with the scheduled sub-transaction")
    deleted: bool = Field(..., description="Whether the scheduled sub-transaction has been deleted")


class TransactionDetail(BaseModel):
    """
    Represents a detailed transaction.
    """
    id: UUID = Field(..., description="The unique identifier of the transaction")
    date: date = Field(..., description="The date of the transaction")
    amount: int = Field(..., description="The amount of the transaction in milliunits")
    memo: Optional[str] = Field(None, description="Memo associated with the transaction")
    cleared: str = Field(..., description="The cleared status of the transaction")
    approved: bool = Field(..., description="Whether the transaction has been approved")
    flag_color: Optional[str] = Field(None, description="Flag color of the transaction")
    account_id: UUID = Field(..., description="The ID of the account associated with the transaction")
    payee_id: Optional[UUID] = Field(None, description="The ID of the payee associated with the transaction")
    category_id: Optional[UUID] = Field(None, description="The ID of the category associated with the transaction")
    deleted: bool = Field(..., description="Whether the transaction has been deleted")


class MonthDetail(BaseModel):
    """
    Represents details of a month in a budget.
    """
    month: date = Field(..., description="The month in YYYY-MM format")
    note: Optional[str] = Field(None, description="Note about the month")
    income: int = Field(..., description="The total income for the month")
    budgeted: int = Field(..., description="The total amount budgeted for the month")
    activity: int = Field(..., description="The total activity for the month")
    to_be_budgeted: int = Field(..., description="The amount left to be budgeted")
    age_of_money: Optional[int] = Field(None, description="The Age of Money as of the month")
    categories: List[Category] = Field(..., description="The list of categories in the month")

