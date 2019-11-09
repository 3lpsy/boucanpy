from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from bountydns.core import logger
from bountydns.broadcast import make_redis, make_broadcast_url
from .base import Base


class HttpRequest(Base):
    __tablename__ = "http_requests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # domain
    path = Column(String, index=True)  # path

    # TODO: add foreign key and relationship and handl cascades, etc
    zone_id = Column(
        ForeignKey("zones.id", ondelete="CASCADE"), index=True, nullable=True
    )
    zone = relationship(
        "bountydns.db.models.zone.Zone",
        foreign_keys="bountydns.db.models.http_request.HttpRequest.zone_id",
        back_populates="dns_requests",
    )

    source_address = Column(String, index=True)
    source_port = Column(Integer)

    type = Column(String, index=True)  # method name

    protocol = Column(String, index=True)  # http or https

    raw_request = Column(Text)

    http_server_id = Column(ForeignKey("http_servers.id"), nullable=False)
    http_server = relationship(
        "bountydns.db.models.http_server.HttpServer",
        foreign_keys="bountydns.db.models.http_request.HttpRequest.http_server_id",
        back_populates="http_requests",
    )

    @staticmethod
    async def on_after_insert(mapper, connection, target):
        logger.info("on_after_insert@http_request.py: Publishing message")
        try:
            publisher = await make_redis()
            res = await publisher.publish_json(
                "channel:auth",
                {"type": "MESSAGE", "name": "HTTP_REQUEST_CREATED", "payload": ""},
            )
        except Exception as e:
            logger.warning(f"on_after_insert error: {str(e)}")
