from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class DnsResponse(Base):
    __tablename__ = "dns_responses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    zone_id = Column(Integer, nullable=True)
    source_address = Column(String, index=True)
    source_port = Column(Integer)
    type = Column(String, index=True)
    protocol = Column(String, index=True)
