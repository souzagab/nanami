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
