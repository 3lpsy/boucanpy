from datetime import datetime
from pydantic import BaseModel


class DnsRequestData(BaseModel):
    id: int
    name: str
    zone_id: int = None
    source_address: str
    source_port: int
    type: str
    protocol: str
    dns_server_name: str
    created_at: datetime
