from typing import Optional, List
from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.zone import Zone
from bountydns.core.entities.zone.data import ZoneData


class ZoneRepo(BaseRepo):
    default_model = Zone
    default_data_model = ZoneData

    def filter_dns_server_name(self, dns_server_name):
        self.filter_or(
            self.model().dns_server_name == dns_server_name,
            self.model().dns_server_name.is_(None),
        )
        return self
