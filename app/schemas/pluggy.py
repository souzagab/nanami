from datetime import date, datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PluggyTransactionsRequestParams(BaseModel):
  """
  Query parameters for listing Pluggy transactions.
  Reference: Based on user-provided image and common Pluggy API patterns.
  - ids: Array of transaction identifiers. If defined, 'from' and 'to' parameters will be discarded by Pluggy.
  - from_date: Filter greater than date. Format (yyyy-mm-dd).
  - to_date: Filter lower than date. Format (yyyy-mm-dd).
  - page_size: Page size for the paging request (default: 20, min: 1, max: 500).
  - page: Page number for the paging request (default: 1, min: 1).
  - bill_id: Credit Card Bill's primary identifier, if account is a credit card.
  - created_at_from: Filter greater than createdAt. Format (yyyy-MM-ddTHH:mm:ss.SSSZ).
  """

  ids: Optional[List[UUID]] = Field(
    default=None,
    description="Array of transaction identifiers. If defined, 'from' and 'to' parameters will be discarded.",
  )
  from_date: Optional[date] = Field(
    default=None, alias="from", description="Filter greater than date. Format (yyyy-mm-dd)."
  )
  to_date: Optional[date] = Field(default=None, alias="to", description="Filter lower than date. Format (yyyy-mm-dd).")
  page_size: Optional[int] = Field(
    default=None,
    alias="pageSize",
    ge=1,
    le=500,
    description="Page size for the paging request, default: API default (often 20 or 50). Min: 1, Max: 500.",
  )
  page: Optional[int] = Field(
    default=None,
    alias="page",
    ge=1,
    description="Page number for the paging request, default: API default (often 1). Min: 1.",
  )
  bill_id: Optional[UUID] = Field(
    default=None, alias="billId", description="Credit Card Bill's primary identifier, if account is a credit card."
  )
  created_at_from: Optional[datetime] = Field(
    default=None, alias="createdAtFrom", description="Filter greater than createdAt. Format (yyyy-MM-ddTHH:mm:ss.SSSZ)."
  )
  # Example: created_at_to: Optional[datetime] = Field(default=None, alias="createdAtTo")

  class Config:
    allow_population_by_field_name = True
    # Ensure that when converting to dict, it respects the alias for query params
    # For sending to httpx, this should be handled by `dict(by_alias=True)`


class PluggyTransactionPaymentDataReceiverDocumentNumber(BaseModel):
  type: Optional[str] = None
  value: Optional[str] = None


class PluggyTransactionPaymentDataReceiver(BaseModel):
  account_number: Optional[str] = Field(default=None, alias="accountNumber")
  branch_number: Optional[str] = Field(default=None, alias="branchNumber")
  document_number: Optional[PluggyTransactionPaymentDataReceiverDocumentNumber] = Field(
    default=None, alias="documentNumber"
  )
  name: Optional[str] = None
  routing_number: Optional[str] = Field(default=None, alias="routingNumber")
  routing_number_ispb: Optional[str] = Field(default=None, alias="routingNumberISPB")


class PluggyTransactionPaymentData(BaseModel):
  payer: Optional[Any] = None  # Using Any as structure is not fully defined by example
  payment_method: Optional[str] = Field(default=None, alias="paymentMethod")
  reason: Optional[str] = None
  receiver: Optional[PluggyTransactionPaymentDataReceiver] = None
  receiver_reference_id: Optional[str] = Field(default=None, alias="receiverReferenceId")
  reference_number: Optional[str] = Field(default=None, alias="referenceNumber")
  boleto_metadata: Optional[Any] = Field(default=None, alias="boletoMetadata")  # Using Any


class PluggyTransaction(BaseModel):
  id: UUID
  description: Optional[str] = None
  description_raw: Optional[str] = Field(default=None, alias="descriptionRaw")
  currency_code: Optional[str] = Field(default=None, alias="currencyCode")
  amount: float
  amount_in_account_currency: Optional[float] = Field(default=None, alias="amountInAccountCurrency")
  date: datetime
  category: Optional[str] = None
  category_id: Optional[str] = Field(default=None, alias="categoryId")
  balance: Optional[float] = None
  account_id: UUID = Field(alias="accountId")
  provider_code: Optional[str] = Field(default=None, alias="providerCode")
  status: Optional[str] = None
  payment_data: Optional[PluggyTransactionPaymentData] = Field(default=None, alias="paymentData")
  type: Optional[str] = None
  operation_type: Optional[str] = Field(default=None, alias="operationType")
  credit_card_metadata: Optional[Any] = Field(default=None, alias="creditCardMetadata")  # Using Any
  acquirer_data: Optional[Any] = Field(default=None, alias="acquirerData")  # Using Any
  merchant: Optional[Any] = None  # Using Any
  provider_id: Optional[str] = Field(default=None, alias="providerId")
  created_at: datetime = Field(alias="createdAt")
  updated_at: datetime = Field(alias="updatedAt")

  class Config:
    allow_population_by_field_name = True


class PluggyTransactionsResponse(BaseModel):
  total: int
  total_pages: int = Field(alias="totalPages")
  page: int
  results: List[PluggyTransaction]

  class Config:
    allow_population_by_field_name = True
