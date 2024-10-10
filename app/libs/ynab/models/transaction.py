from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.ynab.models.category import Category


class TransactionType(str, Enum):
  EXPENSE = "expense"
  INCOME = "income"
  TRANSFER = "transfer"
  DEPOSIT = "deposit"
  WITHDRAWAL = "withdrawal"
  PAYMENT = "payment"
  OTHER = "other"


class Transaction(BaseModel):
  """
  Represents a YNAB transaction.
  """

  id: UUID = Field(..., description="The unique identifier of the transaction")
  date: str = Field(..., description="The date of the transaction")
  amount: int = Field(..., description="The amount of the transaction in milliunits")
  memo: Optional[str] = Field(None, description="A memo for the transaction")
  cleared: str = Field(..., description="The cleared status of the transaction")
  approved: bool = Field(..., description="Whether the transaction is approved")
  flag_color: Optional[str] = Field(None, description="The flag color of the transaction")
  account_id: UUID = Field(..., description="The ID of the account for the transaction")
  payee_id: Optional[UUID] = Field(None, description="The ID of the payee")
  category_id: Optional[UUID] = Field(None, description="The ID of the category")
  transfer_account_id: Optional[UUID] = Field(None, description="The ID of the transfer account")
  transfer_transaction_id: Optional[UUID] = Field(None, description="The ID of the transfer transaction")
  import_id: Optional[str] = Field(None, description="The import ID of the transaction")
  deleted: bool = Field(..., description="Whether the transaction is deleted")
  subtransactions: Optional[List["SubTransaction"]] = Field(None, description="List of subtransactions")
  cleared_at: Optional[str] = Field(None, description="ISO 8601 date when the transaction was cleared")


class CreateTransaction(BaseModel):
  """
  Represents the data required to create a new transaction.
  """

  date: str = Field(..., description="The date of the transaction")
  amount: int = Field(..., description="The amount of the transaction in milliunits")
  memo: Optional[str] = Field(None, description="A memo for the transaction")
  cleared: Optional[str] = Field("uncleared", description="The cleared status of the transaction")
  approved: Optional[bool] = Field(True, description="Whether the transaction is approved")
  flag_color: Optional[str] = Field(None, description="The flag color of the transaction")
  account_id: UUID = Field(..., description="The ID of the account for the transaction")
  payee_id: Optional[UUID] = Field(None, description="The ID of the payee")
  category_id: Optional[UUID] = Field(None, description="The ID of the category")
  transfer_account_id: Optional[UUID] = Field(None, description="The ID of the transfer account")
  import_id: Optional[str] = Field(None, description="The import ID of the transaction")
  subtransactions: Optional[List["CreateSubTransaction"]] = Field(None, description="List of subtransactions")


class UpdateTransaction(BaseModel):
  """
  Represents the data required to update an existing transaction.
  """

  date: Optional[str] = Field(None, description="The date of the transaction")
  amount: Optional[int] = Field(None, description="The amount of the transaction in milliunits")
  memo: Optional[str] = Field(None, description="A memo for the transaction")
  cleared: Optional[str] = Field(None, description="The cleared status of the transaction")
  approved: Optional[bool] = Field(None, description="Whether the transaction is approved")
  flag_color: Optional[str] = Field(None, description="The flag color of the transaction")
  payee_id: Optional[UUID] = Field(None, description="The ID of the payee")
  category_id: Optional[UUID] = Field(None, description="The ID of the category")
  transfer_account_id: Optional[UUID] = Field(None, description="The ID of the transfer account")
  transfer_transaction_id: Optional[UUID] = Field(None, description="The ID of the transfer transaction")
  import_id: Optional[str] = Field(None, description="The import ID of the transaction")
  subtransactions: Optional[List["UpdateSubTransaction"]] = Field(None, description="List of subtransactions")


class SubTransaction(BaseModel):
  """
  Represents a subtransaction in YNAB.
  """

  id: UUID = Field(..., description="The unique identifier of the subtransaction")
  transaction_id: UUID = Field(..., description="The ID of the parent transaction")
  amount: int = Field(..., description="The amount of the subtransaction in milliunits")
  memo: Optional[str] = Field(None, description="A memo for the subtransaction")
  category_id: UUID = Field(..., description="The ID of the category")
  deleted: bool = Field(..., description="Whether the subtransaction is deleted")


class CreateSubTransaction(BaseModel):
  """
  Represents the data required to create a new subtransaction.
  """

  amount: int = Field(..., description="The amount of the subtransaction in milliunits")
  memo: Optional[str] = Field(None, description="A memo for the subtransaction")
  category_id: UUID = Field(..., description="The ID of the category")


class UpdateSubTransaction(BaseModel):
  """
  Represents the data required to update an existing subtransaction.
  """

  amount: Optional[int] = Field(None, description="The amount of the subtransaction in milliunits")
  memo: Optional[str] = Field(None, description="A memo for the subtransaction")
  category_id: Optional[UUID] = Field(None, description="The ID of the category")


class ScheduledTransactionDetail(BaseModel):
  """
  Represents a scheduled transaction.
  """

  id: UUID = Field(..., description="The unique identifier of the scheduled transaction")
  account_id: UUID = Field(..., description="The ID of the account associated with the scheduled transaction")
  date_first: str = Field(..., description="The first date the scheduled transaction is scheduled for")
  date_next: str = Field(..., description="The next date the scheduled transaction is scheduled for")
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
  payee_id: Optional[UUID] = Field(
    None, description="The ID of the payee associated with the scheduled sub-transaction"
  )
  category_id: Optional[UUID] = Field(
    None, description="The ID of the category associated with the scheduled sub-transaction"
  )
  deleted: bool = Field(..., description="Whether the scheduled sub-transaction has been deleted")


class TransactionDetail(BaseModel):
  """
  Represents a detailed transaction.
  """

  id: UUID = Field(..., description="The unique identifier of the transaction")
  date: str = Field(..., description="The date of the transaction")
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

  month: str = Field(..., description="The month in YYYY-MM format")
  note: Optional[str] = Field(None, description="Note about the month")
  income: int = Field(..., description="The total income for the month")
  budgeted: int = Field(..., description="The total amount budgeted for the month")
  activity: int = Field(..., description="The total activity for the month")
  to_be_budgeted: int = Field(..., description="The amount left to be budgeted")
  age_of_money: Optional[int] = Field(None, description="The Age of Money as of the month")
  categories: List[Category] = Field(..., description="The list of categories in the month")


class TransactionsData(BaseModel):
  transactions: List[Transaction]
  server_knowledge: int


class TransactionsResponse(BaseModel):
  data: TransactionsData


class TransactionData(BaseModel):
  transaction: Transaction


class TransactionResponse(BaseModel):
  data: TransactionData


class CreateTransactionResponse(BaseModel):
  data: TransactionData


class UpdateTransactionResponse(BaseModel):
  data: TransactionData
