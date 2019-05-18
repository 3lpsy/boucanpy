from typing import Optional
from pydantic import BaseModel


class ZoneCreateForm(BaseModel):
    domain: str
    ip: str
    dns_server_id: Optional[int]
