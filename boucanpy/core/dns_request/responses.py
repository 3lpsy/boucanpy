from typing import List

from pydantic import BaseModel

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.dns_request.data import DnsRequestData


class DnsRequestResponse(BaseResponse):
    dns_request: DnsRequestData


class DnsRequestsResponse(BaseResponse):
    dns_requests: List[DnsRequestData]
