from typing import List

from pydantic import BaseModel

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.api_token.data import ApiTokenData, SensitiveApiTokenData


class ApiTokenResponse(BaseResponse):
    api_token: ApiTokenData


class ApiTokensResponse(BaseResponse):
    api_tokens: List[ApiTokenData]


class SensitiveApiTokenResponse(BaseResponse):
    api_token: SensitiveApiTokenData
