from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    sub_field = "id"


Base = declarative_base(cls=CustomBase)
metadata = Base.metadata
