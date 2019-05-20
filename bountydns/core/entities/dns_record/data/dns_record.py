from typing import Optional
from pydantic import BaseModel
from bountydns.core.entities.zone import ZoneData


class DnsRecord(BaseModel):
    id: int
    record: str
    zone_id: int
    zone: Optional[ZoneData]
