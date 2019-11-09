import random
import uuid
from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from bountydns.db.models.http_request import HttpRequest
from bountydns.db.factories.http_server import HttpServerFactory
from bountydns.db.factories.zone import ZoneFactory


def random_port():
    return random.randint(1, 65535)


# TODO: get this working
# def random_type():
#     return TYPES.keys()[random.randint(0, len(TYPES.keys()))]


class HttpRequestFactory(BaseFactory):
    class Meta:
        model = HttpRequest

    name = Faker("domain_name")
    path = "/some/fake/path"
    source_address = LazyFunction(fake.ipv4_private)
    source_port = LazyFunction(random_port)
    type = "A"
    protocol = "http"
    http_server = SubFactory(HttpServerFactory)
    zone = SubFactory(ZoneFactory)
    raw_request = "some fake data"
