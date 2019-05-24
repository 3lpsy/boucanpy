from typing import Optional
from pydantic import BaseModel

from bountydns.core.entities.zone.data import ZoneData


class DnsRecordData(BaseModel):
    id: int
    record: str
    sort: int
    zone_id: int
    zone: Optional[ZoneData]
