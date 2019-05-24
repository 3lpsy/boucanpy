from typing import List

from pydantic import BaseModel

from bountydns.core.entities.base.responses import BaseResponse
from bountydns.core.entities.user.data import UserData


class UserResponse(BaseResponse):
    user: UserData


class UsersResponse(BaseResponse):
    users: List[UserData]
