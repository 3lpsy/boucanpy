from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    ip = Column(String, unique=False, index=True)
