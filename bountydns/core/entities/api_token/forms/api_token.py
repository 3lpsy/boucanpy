from pydantic import BaseModel
from datetime import datetime


class ApiTokenCreateForm(BaseModel):
    scopes: str
    expires_at: datetime
    dns_server_name: str
