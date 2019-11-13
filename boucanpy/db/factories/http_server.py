import random
import uuid
from factory import Faker, LazyFunction
from .base import BaseFactory, fake
from boucanpy.db.models.http_server import HttpServer


def get_uuid():
    return str(uuid.uuid4())


class HttpServerFactory(BaseFactory):
    class Meta:
        model = HttpServer

    name = LazyFunction(get_uuid)
