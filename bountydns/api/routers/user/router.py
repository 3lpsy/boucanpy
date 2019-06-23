from typing import List
from fastapi import APIRouter, Depends, Query
from bountydns.db.models.user import User
from bountydns.core.security import ScopedTo, hash_password, TokenPayload, current_user
from bountydns.core import PaginationQS, SortQS, BaseResponse, abort, only
from bountydns.core.user import (
    UserRepo,
    UsersResponse,
    UserResponse,
    UserData,
    UserCreateForm,
    UserEditForm,
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
    token: TokenPayload = Depends(ScopedTo("user:create", "super", satisfy="one")),
):
    # TODO: data validation against current db & perm checks
    data = {
        "email": form.email,
        "hashed_password": hash_password(form.password),
        "is_active": True,
        "is_superuser": getattr(form, "is_superuser", False),
    }
    item = user_repo.create(data).data()
    return UserResponse(user=item)


@router.get("/user/{user_id}", name="user.show", response_model=UserResponse)
async def show(
    user_id: int,
    user_repo: UserRepo = Depends(UserRepo),
    token: TokenPayload = Depends(ScopedTo("user:show", "super")),
    includes: List[str] = Query(None),
):
    includes = only(includes, [], values=True)

    item = user_repo.loads(includes).get_or_fail(user_id).includes(includes).data()
    return UserResponse(user=item)


@router.put("/user/{user_id}", name="user.update", response_model=UserResponse)
async def post(
    user_id: int,
    form: UserEditForm,
    user_repo: UserRepo = Depends(UserRepo),
    token: TokenPayload = Depends(ScopedTo("user:update", "super", satisfy="one")),
):

    data = only(form, ["email", "is_active", "is_superuser"])

    if getattr(form, "password", None):
        data["hashed_password"] = hash_password(form.password)

    item = user_repo.get_or_fail(user_id).update(data).data()
    return UserResponse(user=item)


@router.put(
    "/user/{user_id}/activate", name="user.activate", response_model=UserResponse
)
async def activate(
    user_id: int,
    user_repo: UserRepo = Depends(UserRepo),
    token: TokenPayload = Depends(ScopedTo("user:create", "super")),
):
    user = user_repo.get_or_fail(user_id).update({"is_active": True}).data()
    return UserResponse(user=user)


@router.delete("/user/{user_id}", response_model=BaseResponse)
async def destroy(
    user_id: int,
    user_repo: UserRepo = Depends(UserRepo),
    token: TokenPayload = Depends(ScopedTo("user:create", "super", satisfy="one")),
    user: User = Depends(current_user),
):
    if user_id == user.id:
        abort(403, msg="Cannot deactivate self")

    remaining_supers = len(
        user_repo.filter(
            user_repo.label("is_superuser") == True,
            user_repo.label("is_active") == True,
            user_repo.label("id") != user_id,
        )
        .all()
        .results()
    )

    if remaining_supers < 1:
        abort(403, msg="Cannot deactivate user. No other active super users available.")

    user_repo.clear()

    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not user_repo.exists(id=user_id):
        return BaseResponse(messages=messages)

    user_repo.deactivate(user_id)
    return BaseResponse(messages=messages)
