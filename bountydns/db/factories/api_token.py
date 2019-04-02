import uuid
from datetime import timedelta, datetime
from factory import Faker, LazyFunction
from .base import BaseFactory
from bountydns.db.models.api_token import ApiToken
from bountydns.core.security import create_bearer_token


def random_expires_at():
    expires_delta = timedelta(minutes=3600)
    expire = datetime.utcnow() + expires_delta
    return expire


def bearer_token():
    return str(create_bearer_token(data={"sub": 1}).decode())


class ApiTokenFactory(BaseFactory):
    class Meta:
        model = ApiToken

    scopes = "profile dns-request"
    # TODO: better randomness
    token = LazyFunction(bearer_token)
    is_active = True
    expires_at = LazyFunction(random_expires_at)
    dns_server_name = LazyFunction(uuid.uuid4)
