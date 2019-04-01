from factory import Faker, LazyFunction
from .base import BaseFactory, fake
from bountydns.db.models.zone import Zone


class ZoneFactory(BaseFactory):
    class Meta:
        model = Zone

    domain = Faker("domain_name")
    ip = LazyFunction(fake.ipv4_private)
    is_active = True
