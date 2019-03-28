from typing import Optional, List
from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.zone import Zone


class ZoneRepo(BaseRepo):
    model = Zone
