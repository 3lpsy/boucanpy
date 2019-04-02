from pydantic import BaseModel
from datetime import datetime


class BlackListedTokenData(BaseModel):
    id: int
    token: str
