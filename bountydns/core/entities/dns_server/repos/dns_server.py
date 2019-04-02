from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.dns_request import DnsRequest
from bountydns.db.models.api_token import ApiToken
from bountydns.db.models.zone import Zone
from sqlalchemy.sql.expression import label

from bountydns.core.entities.dns_server.data import DnsServerData
from sqlalchemy.orm import load_only
from sqlalchemy.sql import column


class DnsServerRepo(BaseRepo):
    default_model = None
    default_data_model = DnsServerData

    def create(self, data):
        raise NotImplementedError()

    def to_dict(self, data):
        return {"dns_server_name": data[0]}

    def query(self):
        if not self._query:
            q1 = self.db.query(label("dns_server_name", DnsRequest.dns_server_name))
            q2 = self.db.query(label("dns_server_name", ApiToken.dns_server_name))
            q3 = self.db.query(
                label("dns_server_name", ApiToken.dns_server_name)
            ).filter(ApiToken.dns_server_name.isnot(None))
            u1 = q1.union_all(q2)
            u2 = u1.union_all(q3)
            self._query = u2
        return self._query

    def model(self):
        raise NotImplementedError()
