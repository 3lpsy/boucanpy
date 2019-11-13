from typing import Optional, List
from boucanpy.core.base.repos import BaseRepo
from boucanpy.db.models.zone import Zone
from boucanpy.core.zone.data import ZoneData


class ZoneRepo(BaseRepo):
    default_model = Zone
    default_data_model = ZoneData
