from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    pass


Base = declarative_base(cls=CustomBase)
metadata = Base.metadata
