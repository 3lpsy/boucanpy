from typing import List

from bountydns.core.entities.base.responses import BaseResponse
from bountydns.core.entities.dns_record.data import DnsRecordData


class DnsRecordResponse(BaseResponse):
    dns_record: DnsRecordData


class DnsRecordsResponse(BaseResponse):
    dns_records: List[DnsRecordData]

