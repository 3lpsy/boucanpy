from typing import Optional
from pydantic import BaseModel

# from bountydns.core.zone.data import ZoneData

# TODO: fix circular imports for ZoneData
class DnsRecordData(BaseModel):
    id: int
    record: str
    sort: int
    zone_id: int
    # zone: Optional[ZoneData]
