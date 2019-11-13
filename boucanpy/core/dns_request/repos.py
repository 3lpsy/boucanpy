from boucanpy.core.base.repos import BaseRepo
from boucanpy.db.models.dns_request import DnsRequest
from boucanpy.core.dns_request.data import DnsRequestData


class DnsRequestRepo(BaseRepo):
    default_model = DnsRequest
    default_data_model = DnsRequestData
    default_loads = []
