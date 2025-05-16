from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config.settings import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)

async_session_maker = async_sessionmaker(
  bind=engine,
  expire_on_commit=False,
)
