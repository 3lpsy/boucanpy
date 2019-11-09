from bountydns.core.base.repos import BaseRepo
from bountydns.core.http_server.data import HttpServerData
from bountydns.db.models.http_server import HttpServer


class HttpServerRepo(BaseRepo):
    default_model = HttpServer
    default_data_model = HttpServerData
