from datetime import date, datetime
from typing import List
from uuid import UUID

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.transaction import Transaction


class TransactionRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def create(self, transaction: Transaction) -> Transaction:
    """
    Creates a new transaction in the database.
    Assumes the transaction object is already validated.
    """
    self.session.add(transaction)
    await self.session.commit()
    await self.session.refresh(transaction)
    return transaction

  async def find(self, id: UUID) -> Transaction | None:
    """
    Retrieves a transaction by its primary ID.
    """
    return await self.session.get(Transaction, id)

  async def find_by(self, account_mapping_id: UUID, pluggy_transaction_id: UUID) -> Transaction | None:
    """
    Finds a transaction by its account_mapping_id and pluggy_transaction_id.
    """
    statement = select(Transaction).where(
      Transaction.account_mapping_id == account_mapping_id,
      Transaction.pluggy_transaction_id == pluggy_transaction_id,
    )
    result = await self.session.exec(statement)
    return result.first()

  async def update(self, transaction: Transaction) -> Transaction:
    """
    Updates an existing transaction.
    Assumes the transaction object is managed by the session or needs to be added.
    """
    self.session.add(transaction)  # Ensures the object is tracked if it was detached
    await self.session.commit()
    await self.session.refresh(transaction)
    return transaction

  async def get_unsynced_by_account_id(self, account_mapping_id: UUID) -> List[Transaction]:
    """
    Retrieves all transactions for a given account_mapping_id that have not been synced yet.
    """
    statement = (
      select(Transaction)
      .where(Transaction.account_mapping_id == account_mapping_id)
      .where(Transaction.synced_at.is_(None))  # SQLAlchemy 2.0 style for IS NULL
    )
    result = await self.session.exec(statement)
    return list(result.all())  # Ensure it returns a list

  async def get_latest_synced_transaction_date(self, account_mapping_id: UUID) -> date | None:
    """
    Gets the date of the latest transaction (from its transaction_date field)
    that was successfully synced to YNAB for a given account.
    Returns only the date part.
    """
    statement = (
      select(func.max(Transaction.transaction_date))
      .where(Transaction.account_mapping_id == account_mapping_id)
      .where(Transaction.synced_at.is_not(None))
    )
    result = await self.session.exec(statement)
    max_datetime_val = result.one_or_none()

    if isinstance(max_datetime_val, datetime):
      return max_datetime_val.date()
    elif isinstance(max_datetime_val, date):
      return max_datetime_val
    return None

  async def find_or_create(self, transaction: Transaction) -> Transaction:
    existing_transaction = await self.find_by(
      account_mapping_id=transaction.account_mapping_id,
      pluggy_transaction_id=transaction.pluggy_transaction_id,
    )

    if existing_transaction:
      return existing_transaction

    self.session.add(transaction)
    await self.session.commit()
    await self.session.refresh(transaction)
    return transaction
