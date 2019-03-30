from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo, hash_password
from bountydns.core.entities import (
    UserRepo,
    PaginationQS,
    UsersResponse,
    UserResponse,
    UserData,
    UserCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/user", name="user.index", response_model=UsersResponse)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    user_repo: UserRepo = Depends(UserRepo),
    token: str = ScopedTo("user:list"),
):
    pg, items = user_repo.paginate(pagination).set_data_model(UserData).data()
    return UsersResponse(pagination=pg, users=items)


@router.post("/user", name="user.store", response_model=UserResponse)
async def post(
    form: UserCreateForm,
    user_repo: UserRepo = Depends(UserRepo),
    token: str = ScopedTo("user:create", "super"),
):
    # TODO: data validation against current db & perm checks
    data = {
        "email": form.email,
        "hashed_password": hash_password(form.password),
        "is_active": True,
        "is_superuser": False,
    }
    item = user_repo.create(data).set_data_model(UserData).data()
    return UserResponse(user=item)
