from typing import Optional
from pydantic import BaseModel, ValidationError, validator, constr


class UserCreateForm(BaseModel):
    email: str
    is_superuser: Optional[bool]
    password: constr(min_length=8, max_length=1024)
    password_confirm: constr(min_length=8, max_length=1024)

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
    email: Optional[str]
    is_superuser: Optional[bool]
    password: Optional[constr(min_length=8, max_length=1024)]
    password_confirm: Optional[constr(min_length=8, max_length=1024)]

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
