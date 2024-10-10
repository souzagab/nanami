from typing import Optional

from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel):
  id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

  class Config:
    use_enum_values = True
