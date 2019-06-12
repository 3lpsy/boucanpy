from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from bountydns.core.dns_server.data import DnsServerData

from bountydns.core.dns_record.data import DnsRecordData


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: Optional[int]
    dns_server: Optional[DnsServerData]
    dns_records: Optional[List[DnsRecordData]]
    created_at: datetime
