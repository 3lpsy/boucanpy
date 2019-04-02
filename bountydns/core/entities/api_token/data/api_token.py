from datetime import datetime
from pydantic import BaseModel


class ApiTokenData(BaseModel):
    id: int
    scopes: str
    is_active: bool
    expires_at: datetime
    dns_server_name: str
    created_at: datetime


class SensitiveApiTokenData(ApiTokenData):
    token: str
