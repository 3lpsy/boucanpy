from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: int
    created_at: datetime
