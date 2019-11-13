from typing import List

from pydantic import BaseModel

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.http_request.data import HttpRequestData


class HttpRequestResponse(BaseResponse):
    http_request: HttpRequestData


class HttpRequestsResponse(BaseResponse):
    http_requests: List[HttpRequestData]
