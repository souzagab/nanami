from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base_sql_model import BaseSQLModel

# Avoid importing loop, ensure is just for type checking
if TYPE_CHECKING:
  from app.models.account_reference import AccountReference


class User(BaseSQLModel, table=True):
  __tablename__ = "users"

  account_references: List["AccountReference"] = Relationship(back_populates="user")
