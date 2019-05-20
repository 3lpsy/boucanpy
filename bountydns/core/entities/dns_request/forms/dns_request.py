from pydantic import BaseModel

# TODO: make form custom to dns api client
class DnsRequestCreateForm(BaseModel):
    name: str
    source_address: str
    source_port: int
    type: str
    protocol: str
    dns_server_name: str
