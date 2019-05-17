from typing import Optional, List
from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.zone import Zone
from bountydns.core.entities.zone.data import ZoneData


class ZoneRepo(BaseRepo):
    default_model = Zone
    default_data_model = ZoneData
