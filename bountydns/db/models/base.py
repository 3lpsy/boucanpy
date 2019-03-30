from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import inspect


class CustomBase(object):
    sub_field = "id"

    # TODO: find a better / faster way to do this (register column_attrs at boot ?)
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


Base = declarative_base(cls=CustomBase)
metadata = Base.metadata
