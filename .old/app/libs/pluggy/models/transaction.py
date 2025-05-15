from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class DocumentNumber(BaseModel):
  type: str
  value: str


class Payer(BaseModel):
  accountNumber: Optional[str]
  branchNumber: Optional[str]
  documentNumber: Optional[DocumentNumber]
  name: Optional[str]
  routingNumber: Optional[str]
  routingNumberISPB: Optional[str]


class Receiver(BaseModel):
  accountNumber: Optional[str]
  branchNumber: Optional[str]
  documentNumber: Optional[DocumentNumber]
  name: Optional[str]
  routingNumber: Optional[str]
  routingNumberISPB: Optional[str]


class PaymentData(BaseModel):
  payer: Optional[Payer]
  paymentMethod: Optional[str]
  reason: Optional[str]
  receiver: Optional[Receiver]
  receiverReferenceId: Optional[str]
  referenceNumber: Optional[str]


class Transaction(BaseModel):
  id: str
  description: str
  descriptionRaw: str
  currencyCode: str
  amount: float
  amountInAccountCurrency: Optional[float]
  date: datetime
  category: str
  categoryId: str
  balance: Optional[float]
  accountId: str
  providerCode: Optional[str]
  status: str
  paymentData: Optional[PaymentData]
  type: str
  operationType: Optional[str]
  creditCardMetadata: Optional[str]
  acquirerData: Optional[str]
  merchant: Optional[str]
  createdAt: datetime
  updatedAt: datetime


class ListTransactionsResponse(BaseModel):
  total: int
  totalPages: int
  page: int
  results: List[Transaction]


class GetTransactionResponse(Transaction):
  pass
