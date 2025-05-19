from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.models.account_mapping import AccountMapping
from app.repositories.account_mapping_repository import AccountMappingRepository
from app.schemas.account_mapping import AccountMappingCreate, AccountMappingUpdate


class AccountMappingService:
  def __init__(self, session: AsyncSession):
    self.repository = AccountMappingRepository(session)

  async def get_mapping_by_id(self, mapping_id: UUID) -> AccountMapping | None:
    return await self.repository.get_by_id(mapping_id)

  async def get_all_mappings(self) -> Sequence[AccountMapping]:
    return await self.repository.get_all()

  async def create_mapping(self, mapping_in: AccountMappingCreate) -> AccountMapping:
    return await self.repository.create(mapping_in)

  async def update_mapping(self, mapping_id: UUID, mapping_in: AccountMappingUpdate) -> AccountMapping | None:
    return await self.repository.update(mapping_id, mapping_in)

  async def delete_mapping(self, mapping_id: UUID) -> AccountMapping | None:
    return await self.repository.delete(mapping_id)


# Dependency injector for the service
def get_account_mapping_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> AccountMappingService:
  return AccountMappingService(session)
