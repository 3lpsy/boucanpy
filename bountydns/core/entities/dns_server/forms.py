from pydantic import BaseModel


class DnsServerCreateForm(BaseModel):
    name: str
