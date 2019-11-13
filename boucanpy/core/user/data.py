from datetime import datetime
from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    email: str
    is_superuser: bool
    is_active: bool
    created_at: datetime
