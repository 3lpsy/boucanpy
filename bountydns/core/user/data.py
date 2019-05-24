from datetime import datetime
from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    email: str
    created_at: datetime
