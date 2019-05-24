from typing import List

from pydantic import BaseModel

from bountydns.core.base.responses import BaseResponse
from bountydns.core.dns_request.data import DnsRequestData


class DnsRequestResponse(BaseResponse):
    dns_request: DnsRequestData


class DnsRequestsResponse(BaseResponse):
    dns_requests: List[DnsRequestData]
