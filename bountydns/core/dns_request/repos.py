from bountydns.core.base.repos import BaseRepo
from bountydns.db.models.dns_request import DnsRequest
from bountydns.core.dns_request.data import DnsRequestData


class DnsRequestRepo(BaseRepo):
    default_model = DnsRequest
    default_data_model = DnsRequestData
    default_loads = []
