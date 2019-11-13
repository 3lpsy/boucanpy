from fastapi import APIRouter, Depends
from boucanpy.core.security import ScopedTo, current_user, TokenPayload
from boucanpy.db.models.user import User
from boucanpy.core import PaginationQS, logger
from boucanpy.core.user import UserRepo, UserResponse, UserCreateForm


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
