from factory import Faker
from .base import BaseFactory
from boucanpy.db.models.user import User
from boucanpy.core.security import hash_password


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = Faker("email")
    hashed_password = hash_password("password123")
    email_verified = True
    mfa_secret = ""
    is_active = True
    is_superuser = False
