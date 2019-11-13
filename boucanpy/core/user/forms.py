from typing import Optional
from pydantic import BaseModel, ValidationError, validator, constr
from boucanpy.core import ConstrainedEmailStr, ConstrainedSecretStr


class UserCreateForm(BaseModel):
    email: ConstrainedEmailStr
    is_superuser: Optional[bool]
    password: ConstrainedSecretStr
    password_confirm: ConstrainedSecretStr

    @validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    @validator("email")
    def email_is_lower(cls, v, values, **kwargs):
        if not v:
            return ""
        return v.lower()


class UserEditForm(BaseModel):
    email: Optional[ConstrainedEmailStr]
    is_superuser: Optional[bool]
    password: Optional[ConstrainedSecretStr]
    password_confirm: Optional[ConstrainedSecretStr]

    @validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    @validator("email")
    def email_is_lower(cls, v, values, **kwargs):
        if not v:
            return ""
        return v.lower()
