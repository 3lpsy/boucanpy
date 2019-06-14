from typing import Optional
from pydantic import ConstrainedStr, SecretStr
from pydantic.utils import validate_email
from dnslib import RR
from dnslib.dns import DNSError


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
