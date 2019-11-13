from boucanpy.core.base.repos import BaseRepo
from boucanpy.core.http_server.data import HttpServerData
from boucanpy.db.models.http_server import HttpServer


class HttpServerRepo(BaseRepo):
    default_model = HttpServer
    default_data_model = HttpServerData
