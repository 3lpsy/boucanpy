from sqlalchemy import Column, DateTime, inspect, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from bountydns.db.session import _session


class CustomBase(object):
    __searchable__ = []
    sub_field = "id"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # TODO: find a better / faster way to do this (register column_attrs at boot ?)
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


Base = declarative_base(cls=CustomBase)
metadata = Base.metadata
