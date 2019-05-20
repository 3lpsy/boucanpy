from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from bountydns.db.models.zone import Zone
from bountydns.db.factories.dns_server import DnsServerFactory
from bountydns.db.factories.global_zone import GlobalZoneFactory


class ZoneFactory(GlobalZoneFactory):
    domain = Faker("domain_name")
    ip = Faker("domain_name")
    dns_server = SubFactory(DnsServerFactory)
