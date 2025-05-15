class YNABError(Exception):
  """Base class for YNAB exceptions."""

  def __init__(self, message: str, response=None):
    super().__init__(message)
    self.response = response


class NotFoundError(YNABError):
  """Exception raised for 404 errors."""

  pass


class BadRequestError(YNABError):
  """Exception raised for 400 errors."""

  pass


class YNABClientError(Exception):
  """Base class for YNAB exceptions."""

  def __init__(self, message: str):
    self.message = message


class BudgetNotFoundError(YNABClientError):
  """Exception raised when a budget is not found."""

  def __init__(self, budget_id: str):
    self.message = f"Budget with ID '{budget_id}' not found."


class TransactionNotFoundError(YNABClientError):
  """Exception raised when a transaction is not found."""

  def __init__(self, transaction_id: str):
    self.message = f"Transaction with ID '{transaction_id}' not found."
