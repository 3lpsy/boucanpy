from pydantic import BaseModel, SecretStr, constr
from boucanpy.core import (
    ConstrainedEmailStr,
    ConstrainedSecretStr,
    ConstrainedTokenStr,
)


class PasswordAuthForm(BaseModel):
    username: ConstrainedEmailStr
    password: ConstrainedSecretStr  # TODO: constrain length


class MfaAuthForm(BaseModel):
    token: ConstrainedTokenStr
