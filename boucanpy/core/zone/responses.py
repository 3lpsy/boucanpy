from typing import List

from pydantic import BaseModel

from boucanpy.core.base.responses import BaseResponse
from boucanpy.core.zone.data import ZoneData


class ZoneResponse(BaseResponse):
    zone: ZoneData


class ZonesResponse(BaseResponse):
    zones: List[ZoneData]
