from typing import Optional
from pydantic import BaseModel as PydanticBaseModel


class BaseDataModel(PydanticBaseModel):
    class Config:
        orm_mode = True
