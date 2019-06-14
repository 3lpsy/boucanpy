from pydantic import BaseModel, ValidationError, validator, constr


class UserCreateForm(BaseModel):
    email: str
    password: constr(min_length=8, max_length=1024)
    password_confirm: constr(min_length=8, max_length=1024)

    @validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v
