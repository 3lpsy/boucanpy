from boucanpy.core.base.repos import BaseRepo
from boucanpy.core.dns_server.data import DnsServerData
from boucanpy.db.models.dns_server import DnsServer


class DnsServerRepo(BaseRepo):
    default_model = DnsServer
    default_data_model = DnsServerData
