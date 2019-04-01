from factory import alchemy
from faker import Faker as RealFaker
from faker.providers import internet
from bountydns.db.session import _scoped_session


fake = RealFaker()
fake.add_provider(internet)


class BaseFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = _scoped_session
        sqlalchemy_session_persistence = "commit"
