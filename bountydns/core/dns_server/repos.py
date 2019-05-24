from bountydns.core.base.repos import BaseRepo
from bountydns.core.dns_server.data import DnsServerData
from bountydns.db.models.dns_server import DnsServer


class DnsServerRepo(BaseRepo):
    default_model = DnsServer
    default_data_model = DnsServerData
