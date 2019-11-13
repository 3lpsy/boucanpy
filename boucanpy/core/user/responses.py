from typing import List

from pydantic import BaseModel

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.user.data import UserData


class UserResponse(BaseResponse):
    user: UserData


class UsersResponse(BaseResponse):
    users: List[UserData]
