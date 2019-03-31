from pydantic import BaseModel
from datetime import datetime


class ApiTokenData(BaseModel):
    id: int
    scopes: str
    is_active: bool
    expires_at: datetime


class SensitiveApiTokenData(BaseModel):
    id: int
    token: str
    scopes: str
    is_active: bool
    expires_at: datetime
