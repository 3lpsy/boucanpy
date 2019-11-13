from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from bountydns.core import logger
from bountydns.broadcast import make_redis, make_broadcast_url
from .base import Base


class DnsRequest(Base):
    __tablename__ = "dns_requests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # TODO: add foreign key and relationship and handl cascades, etc
    zone_id = Column(
        ForeignKey("zones.id", ondelete="CASCADE"), index=True, nullable=True
    )
    zone = relationship(
        "bountydns.db.models.zone.Zone",
        foreign_keys="bountydns.db.models.dns_request.DnsRequest.zone_id",
        back_populates="dns_requests",
    )
    source_address = Column(String, index=True)
    source_port = Column(Integer)
    type = Column(String, index=True)
    protocol = Column(String, index=True)
    raw_request = Column(Text)

    dns_server_id = Column(ForeignKey("dns_servers.id"), nullable=False)
    dns_server = relationship(
        "bountydns.db.models.dns_server.DnsServer",
        foreign_keys="bountydns.db.models.dns_request.DnsRequest.dns_server_id",
        back_populates="dns_requests",
    )

    @staticmethod
    async def on_after_insert(mapper, connection, target):
        logger.debug("on_after_insert@DnsRequest: Publishing message")
        try:
            publisher = await make_redis()
            res = await publisher.publish_json(
                "channel:auth",
                {"type": "MESSAGE", "name": "DNS_REQUEST_CREATED", "payload": ""},
            )
        except Exception as e:
            logger.warning(f"on_after_insert error: {str(e)}")
