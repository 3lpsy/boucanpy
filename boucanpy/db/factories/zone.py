from factory import Faker, LazyFunction, SubFactory
from .base import BaseFactory, fake
from boucanpy.db.models.zone import Zone
from boucanpy.db.factories.dns_server import DnsServerFactory
from boucanpy.db.factories.http_server import HttpServerFactory

from boucanpy.db.factories.global_zone import GlobalZoneFactory


class ZoneFactory(GlobalZoneFactory):
    domain = Faker("domain_name")
    ip = Faker("domain_name")
    dns_server = SubFactory(DnsServerFactory)
    http_server = SubFactory(HttpServerFactory)
