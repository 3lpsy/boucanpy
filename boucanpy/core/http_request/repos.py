from boucanpy.core.base.repos import BaseRepo
from boucanpy.db.models.http_request import HttpRequest
from boucanpy.core.http_request.data import HttpRequestData


class HttpRequestRepo(BaseRepo):
    default_model = HttpRequest
    default_data_model = HttpRequestData
    default_loads = []
