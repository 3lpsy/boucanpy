from typing import List, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadDict(BaseModel):
    sub: int = None
    exp: int = None
    scopes: str
    dns_server_name: Optional[str] = ""


class TokenPayload(BaseModel):
    sub: int = None
    exp: int = None
    token: str = ""
    scopes: List[str]
    payload: TokenPayloadDict
