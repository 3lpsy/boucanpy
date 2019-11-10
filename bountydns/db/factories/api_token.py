import uuid
from datetime import timedelta, datetime
from factory import (
    Faker,
    LazyFunction,
    LazyAttribute,
    Sequence,
    lazy_attribute,
    SubFactory,
)
from .base import BaseFactory
from bountydns.db.models.api_token import ApiToken
from bountydns.core.security import create_bearer_token
from bountydns.db.factories.dns_server import DnsServerFactory
from bountydns.db.factories.http_server import HttpServerFactory


def random_expires_at():
    expires_delta = timedelta(minutes=3600)
    expire = datetime.utcnow() + expires_delta
    return expire


def bearer_token(dns_server_name, http_server_name, scopes):
    return str(
        str(
            create_bearer_token(
                data={
                    "sub": 1,
                    "dns_server_name": dns_server_name,
                    "http_server_name": http_server_name,
                    "scopes": scopes,
                }
            )
        )
    )


class ApiTokenFactory(BaseFactory):
    class Meta:
        model = ApiToken

    scopes = "profile dns-request zone:list zone:read"
    # TODO: better randomness
    is_active = True
    expires_at = LazyFunction(random_expires_at)
    dns_server = SubFactory(DnsServerFactory)
    http_server = SubFactory(HttpServerFactory)

    @lazy_attribute
    def token(self):
        return bearer_token(
            str(self.dns_server.name), str(self.http_server.name), str(self.scopes)
        )
