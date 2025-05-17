from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)

# Use SQLAlchemy's async_sessionmaker and tell it to create SQLModel AsyncSession instances
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
  async with async_session_maker() as session:
    yield session
