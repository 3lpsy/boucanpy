from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo
from bountydns.core.entities import UserRepo, PaginationQS, UsersResponse, UserData

router = APIRouter()
options = {"prefix": ""}


@router.get("/user", name="user.index", response_model=UsersResponse)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    user_repo: UserRepo = Depends(UserRepo),
    token: str = ScopedTo("user:list"),
):
    pg, items = user_repo.paginate(pagination)
    items = [UserData(id=i.id, email=i.email) for i in items]
    return UsersResponse(pagination=pg, users=items)
