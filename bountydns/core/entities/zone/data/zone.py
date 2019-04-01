from pydantic import BaseModel


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
