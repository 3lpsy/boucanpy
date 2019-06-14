from pydantic import BaseModel, SecretStr, constr
from bountydns.core import (
    ConstrainedEmailStr,
    ConstrainedSecretStr,
    ConstrainedTokenStr,
)


class PasswordAuthForm(BaseModel):
    username: ConstrainedEmailStr
    password: ConstrainedSecretStr  # TODO: constrain length


class MfaAuthForm(BaseModel):
    token: ConstrainedTokenStr
