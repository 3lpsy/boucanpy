from bountydns.core.base.repos import BaseRepo
from bountydns.db.models.http_request import HttpRequest
from bountydns.core.http_request.data import HttpRequestData


class HttpRequestRepo(BaseRepo):
    default_model = HttpRequest
    default_data_model = HttpRequestData
    default_loads = []
