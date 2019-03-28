from pydantic import BaseModel


class PaginationData(BaseModel):
    page: int
    per_page: int
    total: int
