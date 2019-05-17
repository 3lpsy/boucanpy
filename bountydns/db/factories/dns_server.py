import random
import uuid
from factory import Faker, LazyFunction
from .base import BaseFactory, fake
from bountydns.db.models.dns_server import DnsServer


class DnsServerFactory(BaseFactory):
    class Meta:
        model = DnsServer

    name = LazyFunction(uuid.uuid4)
