from typing import Sequence
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.account_mapping import AccountMapping
from app.schemas.account_mapping import AccountMappingCreate, AccountMappingUpdate


class AccountMappingRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def get_by_id(self, mapping_id: UUID) -> AccountMapping | None:
    return await self.session.get(AccountMapping, mapping_id)

  async def get_all(self) -> Sequence[AccountMapping]:
    statement = select(AccountMapping)
    result = await self.session.exec(statement)
    return result.all()

  async def create(self, mapping_in: AccountMappingCreate) -> AccountMapping:
    db_mapping = AccountMapping.model_validate(mapping_in)
    self.session.add(db_mapping)
    await self.session.commit()
    await self.session.refresh(db_mapping)
    return db_mapping

  async def update(self, mapping_id: UUID, mapping_in: AccountMappingUpdate) -> AccountMapping | None:
    db_mapping = await self.get_by_id(mapping_id)
    if not db_mapping:
      return None

    update_data = mapping_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
      setattr(db_mapping, key, value)

    self.session.add(db_mapping)
    await self.session.commit()
    await self.session.refresh(db_mapping)
    return db_mapping

  async def delete(self, mapping_id: UUID) -> AccountMapping | None:
    db_mapping = await self.get_by_id(mapping_id)
    if not db_mapping:
      return None
    await self.session.delete(db_mapping)
    await self.session.commit()
    return db_mapping
