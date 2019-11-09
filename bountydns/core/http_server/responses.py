from typing import List

from pydantic import BaseModel

from bountydns.core.base.responses import BaseResponse
from bountydns.core.dns_server.data import DnsServerData


class DnsServerResponse(BaseResponse):
    dns_server: DnsServerData


class DnsServersResponse(BaseResponse):
    dns_servers: List[DnsServerData]
