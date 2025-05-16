import datetime

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
  id: int = Field(index=True, primary_key=True, nullable=False)

  created_at: datetime = Field(default_factory=datetime.now, nullable=False)
  updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

  class Config:
    use_enum_values = True
