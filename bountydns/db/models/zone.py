from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from bountydns.core import logger
from bountydns.broadcast import make_redis, make_broadcast_url

from .base import Base


class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    ip = Column(String, unique=False, index=True)
    is_active = Column(Boolean(), default=True)
    dns_server_name = Column(String, nullable=True)
    dns_requests = relationship(
        "bountydns.db.models.dns_request.DnsRequest",
        foreign_keys="bountydns.db.models.dns_request.DnsRequest.zone_id",
        back_populates="zone",
    )

    @staticmethod
    async def on_after_insert(mapper, connection, target):
        logger.warning("on_after_insert: Zone")
        print("on_after_insert", mapper, connection, target)
        publisher = await make_redis()
        res = await publisher.publish_json(
            "channel:auth", {"type": "MESSAGE", "name": "ZONE_CREATED", "payload": ""}
        )
