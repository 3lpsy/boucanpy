from factory import Faker
from .user import UserFactory
from boucanpy.db.models.user import User
from boucanpy.core.security import hash_password


class SuperUserFactory(UserFactory):
    is_superuser = True
