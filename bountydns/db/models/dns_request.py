from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from .base import Base


class DnsRequest(Base):
    __tablename__ = "dns_requests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # TODO: add foreign key and relationship and handl cascades, etc
    zone_id = Column(ForeignKey("zones.id", ondelete="CASCADE"), index=True)
    zone = relationship(
        "bountydns.db.models.zone.Zone",
        foreign_keys="bountydns.db.models.dns_request.DnsRequest.zone_id",
        back_populates="dns_requests",
    )
    source_address = Column(String, index=True)
    source_port = Column(Integer)
    type = Column(String, index=True)
    protocol = Column(String, index=True)
    dns_server_name = Column(String, index=True)
