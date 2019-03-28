from typing import List

from pydantic import BaseModel

from bountydns.core.entities.base.responses import BaseResponse
from bountydns.core.entities.zone.data import ZoneData


class ZoneResponse(BaseResponse):
    zone: ZoneData


class ZonesResponse(BaseResponse):
    zones: List[ZoneData]
