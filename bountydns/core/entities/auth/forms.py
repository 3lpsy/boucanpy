from pydantic import BaseModel, SecretStr


class PasswordAuthForm(BaseModel):
    username: str
    password: SecretStr


class MfaAuthForm(BaseModel):
    token: SecretStr
