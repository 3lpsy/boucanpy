from typing import List

from pydantic import BaseModel

from bountydns.core.base.responses import BaseResponse
from bountydns.core.user.data import UserData


class UserResponse(BaseResponse):
    user: UserData


class UsersResponse(BaseResponse):
    users: List[UserData]
