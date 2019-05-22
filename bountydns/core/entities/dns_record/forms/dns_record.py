from pydantic import BaseModel
from dnslib import RR
from dnslib.dns import DNSError


class DnsRecordStr(str):
    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            RR.fromZone(v)
        except Exception as e:
            msg = str(e)
            raise ValueError(f"could not cast record: {msg}")
        return v


class DnsRecordCreateForm(BaseModel):
    record: DnsRecordStr
    sort: int
    zone_id: int


class DnsRecordForZoneCreateForm(BaseModel):
    record: DnsRecordStr
    sort: int
