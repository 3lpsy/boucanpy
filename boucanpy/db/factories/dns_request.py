import random
import uuid
from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from boucanpy.db.models.dns_request import DnsRequest
from boucanpy.dns.types import TYPES
from boucanpy.db.factories.dns_server import DnsServerFactory
from boucanpy.db.factories.zone import ZoneFactory


def random_port():
    return random.randint(1, 65535)


# TODO: get this working
# def random_type():
#     return TYPES.keys()[random.randint(0, len(TYPES.keys()))]


class DnsRequestFactory(BaseFactory):
    class Meta:
        model = DnsRequest

    name = Faker("domain_name")
    source_address = LazyFunction(fake.ipv4_private)
    source_port = LazyFunction(random_port)
    type = "A"
    protocol = "udp"
    dns_server = SubFactory(DnsServerFactory)
    zone = SubFactory(ZoneFactory)
    raw_request = "some fake data"
