from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Credential(BaseModel):
    validation: str
    validationMessage: str
    label: str
    name: str
    type: str
    placeholder: Optional[str]
    optional: bool


class HealthStatus(BaseModel):
    status: str
    stage: Optional[str]


class Connector(BaseModel):
    id: int
    name: str
    primaryColor: str
    institutionUrl: HttpUrl
    country: str
    type: str
    credentials: List[Credential]
    imageUrl: HttpUrl
    hasMFA: bool
    oauth: bool
    health: HealthStatus
    products: List[str]
    createdAt: str
    isSandbox: bool
    isOpenFinance: bool
    updatedAt: str
    supportsPaymentInitiation: bool
    supportsScheduledPayments: bool
    supportsSmartTransfers: bool


class StatusDetailSub(BaseModel):
    warnings: Optional[List[str]]
    isUpdated: Optional[bool]
    lastUpdatedAt: Optional[str]


class StatusDetail(BaseModel):
    loans: Optional[str]
    accounts: Optional[StatusDetailSub]
    benefits: Optional[str]
    identity: Optional[StatusDetailSub]
    portfolio: Optional[str]
    creditCards: Optional[StatusDetailSub]
    investments: Optional[StatusDetailSub]
    paymentData: Optional[str]
    transactions: Optional[StatusDetailSub]
    incomeReports: Optional[str]
    opportunities: Optional[str]
    investmentTransactions: Optional[str]


class Item(BaseModel):
    id: str
    connector: Connector
    createdAt: str
    updatedAt: str
    status: str
    executionStatus: str
    lastUpdatedAt: str
    webhookUrl: Optional[HttpUrl]
    error: Optional[str]
    clientUserId: str
    consecutiveFailedLoginAttempts: int
    statusDetail: StatusDetail
    parameter: Optional[str]
    userAction: Optional[str]
    nextAutoSyncAt: Optional[str]
    consentExpiresAt: Optional[str]
    products: List[str]
    oauthRedirectUri: Optional[HttpUrl]
