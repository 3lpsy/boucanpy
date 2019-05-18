from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from bountydns.db.models.zone import Zone
from bountydns.db.factories.dns_server import DnsServerFactory


class GlobalZoneFactory(BaseFactory):
    class Meta:
        model = Zone

    domain = Faker("domain_name")
    ip = LazyFunction(fake.ipv4_private)
    is_active = True
