from typing import List, Optional

from pydantic import BaseModel
from bountydns.core.entities.pagination.responses import PaginationResponse


class MessageResponse(BaseModel):
    text: str
    type: str


class BaseResponse(BaseModel):
    messages: List[MessageResponse] = []
    pagination: Optional[PaginationResponse] = None
