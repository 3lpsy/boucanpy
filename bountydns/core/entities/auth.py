from pydantic import BaseModel


class AuthSubmission(BaseModel):
    email: str
    password: str


class MfaAuthSubmission(BaseModel):
    token: str
