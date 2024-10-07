from sqlmodel import Field, Relationship

from app.models.base_sql_model import BaseSQLModel
from app.models.user import User


# Link between YNAB Account and Pluggy Account
class AccountReference(BaseSQLModel, table=True):
  __tablename__ = "account_references"

  name: str = Field(default=None, nullable=False)

  external_source_id: str = Field(default=None, index=True, description="Open finance / Pluggy API Item ref")
  external_destination_id: str = Field(default=None, index=True, description="YNAB Account reference")

  user_id: int = Field(default=None, foreign_key="users.id")
  user: User = Relationship(back_populates="account_references")
