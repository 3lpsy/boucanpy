from pydantic import BaseModel


class ZoneCreateForm(BaseModel):
    domain: str
    ip: str
