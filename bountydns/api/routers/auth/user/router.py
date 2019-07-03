from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo, current_user, TokenPayload
from bountydns.db.models.user import User
from bountydns.core import PaginationQS, logger
from bountydns.core.user import UserRepo, UserResponse, UserCreateForm


router = APIRouter()
options = {"prefix": "/auth"}


@router.get("/user", name="auth.user.show", response_model=UserResponse)
async def show(
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("profile")),
    user: User = Depends(current_user),
):
    logger.critical("Loading user")
    item = user_repo.set_results(user).data()
    return UserResponse(user=item)
