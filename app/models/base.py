import datetime
import uuid

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)

  created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
  updated_at: datetime.datetime = Field(
    default_factory=datetime.datetime.utcnow, sa_column_kwargs={"onupdate": datetime.datetime.utcnow}
  )

  class Config:
    use_enum_values = True
