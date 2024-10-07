from typing import Optional

from pydantic import BaseModel, HttpUrl


class AuthRequest(BaseModel):
  clientId: str
  clientSecret: str


class AuthResponse(BaseModel):
  apiKey: str


class ConnectTokenOptions(BaseModel):
  webhookUrl: Optional[HttpUrl]
  clientUserId: Optional[str]


class ConnectTokenRequest(BaseModel):
  itemId: str
  options: Optional[ConnectTokenOptions]


class ConnectTokenResponse(BaseModel):
  accessToken: str
