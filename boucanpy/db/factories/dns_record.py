import random
import uuid
from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from boucanpy.db.models.dns_record import DnsRecord
from boucanpy.dns.types import TYPES
from boucanpy.db.factories.dns_server import DnsServerFactory
from boucanpy.db.factories.zone import ZoneFactory


def random_record():
    return f"@ IN  A  {fake.ipv4()}."


def random_sort():
    return random.randint(0, 10)


class DnsRecordFactory(BaseFactory):
    class Meta:
        model = DnsRecord

    record = LazyFunction(random_record)
    sort = LazyFunction(random_sort)
    zone = SubFactory(ZoneFactory)
