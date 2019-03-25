from pydantic import BaseModel


class PasswordAuthForm(BaseModel):
    email: str
    password: str


class MfaAuthForm(BaseModel):
    token: str
