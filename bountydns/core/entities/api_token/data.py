from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from bountydns.core.entities.dns_server import DnsServerData


class ApiTokenData(BaseModel):
    id: int
    scopes: str
    is_active: bool
    expires_at: datetime
    dns_server_id: int
    dns_server: Optional[DnsServerData]
    created_at: datetime


class SensitiveApiTokenData(ApiTokenData):
    token: str
