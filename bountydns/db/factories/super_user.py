from factory import Faker
from .user import UserFactory
from bountydns.db.models.user import User
from bountydns.core.security import hash_password


class SuperUserFactory(UserFactory):
    is_superuser = True
