from datetime import datetime
from pydantic import BaseModel


class DnsServerData(BaseModel):
    name: str
