from typing import Optional
from pydantic import BaseModel, validator
from bountydns.core import is_valid_domain, is_valid_ipv4address


class ZoneCreateForm(BaseModel):
    domain: str
    ip: str
    dns_server_id: Optional[int]

    @validator("ip")
    def check_is_valid_ipv4address(cls, v):
        if not is_valid_ipv4address(v):
            raise ValueError(f"ip must be in a valid IPv4Address format")
        return v

    @validator("domain")
    def check_is_valid_domain(cls, v):
        if not is_valid_domain(v):
            raise ValueError(f"domain must be in a valid domain format")
        return v.lower()
