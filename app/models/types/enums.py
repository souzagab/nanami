import enum


class AccountMappingStatus(str, enum.Enum):
  ACTIVE = "ACTIVE"
  INACTIVE = "INACTIVE"
  ARCHIVED = "ARCHIVED"


class AccountMappingType(str, enum.Enum):
  CHECKING = "CHECKING"
  SAVINGS = "SAVINGS"
  CREDIT_CARD = "CREDIT_CARD"
  INVESTMENT = "INVESTMENT"
  LOAN = "LOAN"
  OTHER = "OTHER"
