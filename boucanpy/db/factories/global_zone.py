from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from boucanpy.db.models.zone import Zone
from boucanpy.db.factories.dns_server import DnsServerFactory


class GlobalZoneFactory(BaseFactory):
    class Meta:
        model = Zone

    domain = Faker("domain_name")
    ip = LazyFunction(fake.ipv4_private)
    is_active = True
