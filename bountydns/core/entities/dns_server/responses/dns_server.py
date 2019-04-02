from typing import List

from pydantic import BaseModel

from bountydns.core.entities.base.responses import BaseResponse
from bountydns.core.entities.dns_server.data import DnsServerData


class DnsServerResponse(BaseResponse):
    dns_server: DnsServerData


class DnsServersResponse(BaseResponse):
    dns_servers: List[DnsServerData]
