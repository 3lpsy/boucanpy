from typing import List

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.dns_record.data import DnsRecordData


class DnsRecordsDigResponse(BaseResponse):
    dig: str


class DnsRecordResponse(BaseResponse):
    dns_record: DnsRecordData


class DnsRecordsResponse(BaseResponse):
    dns_records: List[DnsRecordData]
