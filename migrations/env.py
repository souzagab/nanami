import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
  fileConfig(config.config_file_name)

from app.models import *  # noqa

target_metadata = SQLModel.metadata

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
  raise ValueError("DATABASE_URL environment variable is not set.")


def run_migrations_offline():
  """Run migrations in 'offline' mode."""
  url = DATABASE_URL
  context.configure(
    url=url,
    target_metadata=target_metadata,
    literal_binds=True,
    dialect_opts={"paramstyle": "named"},
  )

  with context.begin_transaction():
    context.run_migrations()

  with context.begin_transaction():
    context.run_migrations()


def do_run_migrations(connection: Connection):
  context.configure(connection=connection, target_metadata=target_metadata)

  with context.begin_transaction():
    context.run_migrations()


async def run_async_migrations() -> None:
  """In this scenario we need to create an Engine
  and associate a connection with the context.

  """

  connectable = create_async_engine(DATABASE_URL, echo=True, future=True)

  async with connectable.connect() as connection:
    await connection.run_sync(do_run_migrations)

  await connectable.dispose()


if context.is_offline_mode():
  run_migrations_offline()
else:
  asyncio.run(run_async_migrations())
