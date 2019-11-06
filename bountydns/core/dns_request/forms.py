from pydantic import BaseModel, constr, conint

# TODO: make form custom to dns api client
class DnsRequestCreateForm(BaseModel):
    name: constr(min_length=4, max_length=2048)
    source_address: constr(min_length=7, max_length=15)
    source_port: conint(ge=0, le=65535)
    type: constr(min_length=1, max_length=32)
    protocol: constr(min_length=3, max_length=5)
    dns_server_name: constr(regex="^[a-zA-Z0-9-_]+$", min_length=4, max_length=254)
    raw_request: constr(min_length=1, max_length=16384)
