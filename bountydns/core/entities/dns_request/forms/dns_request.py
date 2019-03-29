from pydantic import BaseModel


class DnsRequestCreateForm(BaseModel):
    id: int
    name: str
    source_address: str
    source_port: int
    type: str
    protocol: str
