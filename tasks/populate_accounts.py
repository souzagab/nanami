import os
import sys
from typing import Optional

from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Correct import path
from app.models import User, AccountReference

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
  logger.error("DATABASE_URL environment variable is not set.")
  raise ValueError("DATABASE_URL environment variable is not set.")


engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_session_maker = async_sessionmaker(
  bind=engine,
  expire_on_commit=False,
)

account_refs = [
  {
    "name": "Santander",
    "item_id": "987b4345-5fc2-4460-9b7c-6e3633b62410",
    "account_id": "0a348dd6-b858-4d9c-9bd3-e4256f7549d6",
    "payee_id": "0a348dd6-b858-4d9c-9bd3-e4256f7549d6",
  },
  {
    "name": "Sicoob",
    "item_id": "12c92a9d-f08c-42d0-a433-a57c2d192ff3",
    "account_id": "c4223481-e8cd-4b6e-8d33-c9d2b128f4e0",
    "payee_id": "c4223481-e8cd-4b6e-8d33-c9d2b128f4e0",
  },
  {
    "name": "Nubank",
    "item_id": "7f89ea99-30a0-4ac8-9aa4-7541f9c70606",
    "account_id": "da85cb40-299b-4096-902c-a06343af0968",
    "payee_id": "da85cb40-299b-4096-902c-a06343af0968",
  },
  {
    "name": "Nubank Empresarial",
    "item_id": "1443ef3c-da48-478c-87c1-92f4d0043a3e",
    "account_id": "7d5e40c8-a1e2-46d0-ba92-a41662cb3025",
    "payee_id": "7d5e40c8-a1e2-46d0-ba92-a41662cb3025",
  },
  {
    "name": "Sicoob Empresarial",
    "item_id": "32fa14c0-088d-45d3-a277-d9a131c142dd",
    "account_id": "e5d9d172-4b01-4c91-9b7e-bac29666be66",
    "payee_id": "17e1763f-ee95-4a77-9556-1b9db3f8314d",
  },
  {
    "name": "Nubank Empresarial - Cartão de crédito",
    "item_id": "1dbc29ce-fbbc-4dee-a39c-a802658fc499",
    "account_id": "c8f6885c-6e47-4d24-a98b-947c152a98b8",
    "payee_id": "c8f6885c-6e47-4d24-a98b-947c152a98b8",
  },
  {
    "name": "Santander - Cartão de crédito",
    "item_id": "9496176d-e314-42ca-be57-a78c2731f75c",
    "account_id": "64f10ae3-bc46-46f2-be32-5393f40347b1",
    "payee_id": "64f10ae3-bc46-46f2-be32-5393f40347b1",
  },
  {
    "name": "Sicoob - Cartão de crédito",
    "item_id": "b4175015-3b22-48e6-a37c-b4ab04f47410",
    "account_id": "3c0b387e-ab3a-4b13-967d-62bff6cf605d",
    "payee_id": "3c0b387e-ab3a-4b13-967d-62bff6cf605d",
  },
  {
    "name": "Nubank - Cartão de Crédito",
    "item_id": "425d09f7-c348-47b0-95ec-a28dde352e87",
    "account_id": "974a753e-fa39-4d8f-a7b2-d7d1f5bbb5f5",
    "payee_id": "974a753e-fa39-4d8f-a7b2-d7d1f5bbb5f5",
  },
]

async def create_account_reference(
    name: str,
    external_source_id: str,
    external_destination_id: str,
    external_destination_payee_id: str,
    user_id: int
) -> AccountReference:
  """
  Create a new AccountReference record.
  """
  account_ref = AccountReference(
    name=name,
    external_source_id=external_source_id,
    external_destination_id=external_destination_id,
    external_destination_payee_id=external_destination_payee_id,
    external_destination_budget_id="6bb679ae-8af7-4980-8e4c-2f90ee226577",
    user_id=user_id
  )
  return account_ref


async def create_user() -> int:
  async with async_session_maker() as session:
    async with session.begin():
      user = User()
      session.add(user)
      await session.flush()
      logger.info(f"Created User with ID: {user.id}")
      return user.id

async def create_accounts(user_id: int):
  async with async_session() as session:
    async with session.begin():


      for ref in account_refs:
        account_ref = await create_account_reference(
          name=ref["name"],
          external_source_id=ref["item_id"],
          external_destination_id=ref["account_id"],
          external_destination_payee_id=ref["payee_id"],
          user_id=user_id
        )
        session.add(account_ref)
        logger.info(f"Added AccountReference: {account_ref.name}")

    # Commit is handled by the context manager; no need to call session.commit() here
    logger.info("All AccountReference records have been successfully added to the database.")


async def main():
  try:
    # Create a new user and get the user ID
    user_id = await create_user()

    # Create AccountReference records associated with the user
    await create_accounts(user_id)

  except Exception as e:
    logger.exception("An error occurred while populating the database.")
    raise e

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
