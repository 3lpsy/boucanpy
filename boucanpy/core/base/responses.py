from typing import List, Optional

from pydantic import BaseModel
from boucanpy.core.pagination.responses import PaginationResponse


class MessageResponse(BaseModel):
    text: str
    type: str


class BaseResponse(BaseModel):
    messages: List[MessageResponse] = []
    pagination: Optional[PaginationResponse] = None
