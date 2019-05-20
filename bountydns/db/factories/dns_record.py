import random
import uuid
from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from bountydns.db.models.dns_record import DnsRecord
from bountydns.dns.types import TYPES
from bountydns.db.factories.dns_server import DnsServerFactory
from bountydns.db.factories.zone import ZoneFactory


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
