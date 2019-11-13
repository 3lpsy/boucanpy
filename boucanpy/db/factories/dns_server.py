import random
import uuid
from factory import Faker, LazyFunction
from .base import BaseFactory, fake
from boucanpy.db.models.dns_server import DnsServer


def get_uuid():
    return str(uuid.uuid4())


class DnsServerFactory(BaseFactory):
    class Meta:
        model = DnsServer

    name = LazyFunction(get_uuid)
