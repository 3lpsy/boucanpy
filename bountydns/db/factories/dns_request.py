import random
import uuid
from factory import Faker, LazyFunction
from .base import BaseFactory, fake
from bountydns.db.models.dns_request import DnsRequest
from bountydns.dns.types import TYPES


def random_port():
    return random.randint(1, 65535)


# TODO: get this working
# def random_type():
#     return TYPES.keys()[random.randint(0, len(TYPES.keys()))]


class DnsRequestFactory(BaseFactory):
    class Meta:
        model = DnsRequest

    name = Faker("domain_name")
    zone_id = None
    source_address = LazyFunction(fake.ipv4_private)
    source_port = LazyFunction(random_port)
    type = "A"
    protocol = "udp"
    dns_server_name = LazyFunction(uuid.uuid4)
