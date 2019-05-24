from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from bountydns.core.entities.dns_server.data import DnsServerData

from bountydns.core.entities.dns_record.data import DnsRecordData


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: Optional[int]
    dns_server: Optional[DnsServerData]
    dns_records: Optional[DnsRecordData]
    created_at: datetime
