from typing import Optional
from pydantic import BaseModel


class PasswordAuthResponse(BaseModel):
    token_type: str
    access_token: str
    ws_access_token: Optional[str]
