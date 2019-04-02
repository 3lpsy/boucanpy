from datetime import datetime
from pydantic import BaseModel


class DnsServerData(BaseModel):
    dns_server_name: str
