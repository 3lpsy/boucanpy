from typing import List

from pydantic import BaseModel

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.http_server.data import HttpServerData


class HttpServerResponse(BaseResponse):
    http_server: HttpServerData


class HttpServersResponse(BaseResponse):
    http_servers: List[HttpServerData]
