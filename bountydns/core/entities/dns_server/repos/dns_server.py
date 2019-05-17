from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.dns_request import DnsRequest
from bountydns.db.models.api_token import ApiToken
from bountydns.db.models.zone import Zone
from sqlalchemy.sql.expression import label

from bountydns.core.entities.dns_server.data import DnsServerData
from bountydns.db.models.dns_server import DnsServer
from sqlalchemy.orm import load_only
from sqlalchemy.sql import column


class DnsServerRepo(BaseRepo):
    default_model = DnsServer
    default_data_model = DnsServerData
