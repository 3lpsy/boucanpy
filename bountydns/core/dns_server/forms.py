from pydantic import BaseModel, constr


class DnsServerCreateForm(BaseModel):
    name: constr(regex="^[a-zA-Z0-9-_]+$", min_length=4, max_length=254)
