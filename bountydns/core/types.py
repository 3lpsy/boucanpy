from typing import Optional, List, ForwardRef
from pydantic import ConstrainedStr, SecretStr, BaseModel
from pydantic.utils import validate_email
from dnslib import RR
from dnslib.dns import DNSError
from datetime import datetime


class ConstrainedSecretStr(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 1024

    @classmethod
    def validate(cls, value: str) -> "SecretStr":
        return cls(value)

    def __init__(self, value: str):
        self._secret_value = value

    def __repr__(self) -> str:
        return "SecretStr('**********')" if self._secret_value else "SecretStr('')"

    def __str__(self) -> str:
        return self.__repr__()

    def display(self) -> str:
        return "**********" if self._secret_value else ""

    def get_secret_value(self) -> str:
        return self._secret_value


class ConstrainedTokenStr(ConstrainedSecretStr):
    max_length: Optional[int] = 2048


class ConstrainedEmailStr(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 255

    @classmethod
    def validate(cls, v):
        v = super().validate(v)
        return validate_email(v)[1]


class DnsRecordStr(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 1024

    @classmethod
    def validate(cls, v):
        v = super().validate(v)
        try:
            RR.fromZone(v)
        except Exception as e:
            msg = str(e)
            raise ValueError(f"could not cast record: {msg}")
        return v


class DnsServerData(BaseModel):
    id: int
    name: str
    zones: Optional[List[ForwardRef("ZoneData")]]
    created_at: datetime


class HttpServerData(BaseModel):
    id: int
    name: str
    zones: Optional[List[ForwardRef("ZoneData")]]
    created_at: datetime


class DnsRecordData(BaseModel):
    id: int
    record: str
    sort: int
    zone_id: int
    # zone: Optional[ZoneData]


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: Optional[int]
    dns_server: Optional[DnsServerData]
    dns_records: Optional[List[DnsRecordData]]
    http_server_id: Optional[int]
    http_server: Optional[HttpServerData]
    created_at: datetime


class DnsRequestData(BaseModel):
    id: int
    name: str
    zone_id: int = None
    source_address: str
    source_port: int
    type: str
    protocol: str
    dns_server_id: int
    created_at: datetime
    raw_request: str
    dns_server: Optional[DnsServerData]


class HttpRequestData(BaseModel):
    id: int
    name: str
    path: str
    zone_id: int = None
    source_address: str
    source_port: int
    type: str
    protocol: str
    raw_request: str
    http_server_id: int
    http_server: Optional[HttpServerData]
    created_at: datetime


class ApiTokenData(BaseModel):
    id: int
    scopes: str
    is_active: bool
    expires_at: datetime
    dns_server_id: int
    dns_server: Optional[DnsServerData]
    created_at: datetime


class SensitiveApiTokenData(ApiTokenData):
    token: str


DnsServerData.update_forward_refs()
HttpServerData.update_forward_refs()
