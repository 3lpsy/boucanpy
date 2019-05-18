from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from bountydns.core.entities.dns_server.data import DnsServerData


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: Optional[int]
    dns_server: Optional[DnsServerData]
    created_at: datetime
