import uuid
from datetime import timedelta, datetime
from factory import Faker, LazyFunction
from .base import BaseFactory
from bountydns.db.models.api_token import ApiToken


def random_expires_at():
    expires_delta = timedelta(minutes=3600)
    expire = datetime.utcnow() + expires_delta
    return expire


class ApiTokenFactory(BaseFactory):
    class Meta:
        model = ApiToken

    scopes = "profile dns-request"
    # TODO: better randomness
    token = LazyFunction(uuid.uuid4)
    is_active = True
    expires_at = LazyFunction(random_expires_at)
