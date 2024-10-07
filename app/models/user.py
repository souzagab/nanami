from app.models.base_sql_model import BaseSQLModel


class User(BaseSQLModel, table=True):
  __tablename__ = "users"
