from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class HttpServer(Base):
    __tablename__ = "http_servers"
    __searchable__ = ["name"]
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    api_tokens = relationship(
        "bountydns.db.models.api_token.ApiToken",
        foreign_keys="bountydns.db.models.api_token.ApiToken.http_server_id",
        back_populates="http_server",
    )

    zones = relationship(
        "bountydns.db.models.zone.Zone",
        foreign_keys="bountydns.db.models.zone.Zone.http_server_id",
        back_populates="http_server",
    )

    http_requests = relationship(
        "bountydns.db.models.http_request.HttpRequest",
        foreign_keys="bountydns.db.models.http_request.HttpRequest.http_server_id",
        back_populates="http_server",
    )
