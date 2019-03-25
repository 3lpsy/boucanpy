from pydantic import BaseModel


class PasswordAuthResponse(BaseModel):
    token_type: str
    access_token: str
