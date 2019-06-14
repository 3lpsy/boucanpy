from pydantic import BaseModel, constr
from datetime import datetime


class ApiTokenCreateForm(BaseModel):
    scopes: constr(min_length=4, max_length=1024)
    expires_at: datetime
    dns_server_id: int
