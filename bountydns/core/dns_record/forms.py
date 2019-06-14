from pydantic import BaseModel, conint
from bountydns.core import DnsRecordStr


class DnsRecordCreateForm(BaseModel):
    record: DnsRecordStr
    sort: conint(ge=0, le=1024)
    zone_id: int


class DnsRecordForZoneCreateForm(BaseModel):
    record: DnsRecordStr
    sort: conint(ge=0, le=1024)
