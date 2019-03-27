from pydantic import BaseModel


class PasswordAuthForm(BaseModel):
    username: str
    password: str


class MfaAuthForm(BaseModel):
    token: str
