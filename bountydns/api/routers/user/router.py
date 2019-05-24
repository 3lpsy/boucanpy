from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo, hash_password, TokenPayload
from bountydns.core import PaginationQS, SortQS
from bountydns.core.user import (
    UserRepo,
    UsersResponse,
    UserResponse,
    UserData,
    UserCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/user", name="user.index", response_model=UsersResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    user_repo: UserRepo = Depends(UserRepo),
    token: TokenPayload = Depends(ScopedTo("user:list")),
):
    pg, items = user_repo.sort(sort_qs).paginate(pagination).data()
    return UsersResponse(pagination=pg, users=items)


@router.post("/user", name="user.store", response_model=UserResponse)
async def post(
    form: UserCreateForm,
    user_repo: UserRepo = Depends(UserRepo),
    token: TokenPayload = Depends(ScopedTo("user:create", "super")),
):
    # TODO: data validation against current db & perm checks
    data = {
        "email": form.email,
        "hashed_password": hash_password(form.password),
        "is_active": True,
        "is_superuser": False,
    }
    item = user_repo.create(data).data()
    return UserResponse(user=item)
