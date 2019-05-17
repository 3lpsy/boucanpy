from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class DnsServer(Base):
    __tablename__ = "dns_servers"
    __searchable__ = ["name"]
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    api_tokens = relationship(
        "bountydns.db.models.api_token.ApiToken",
        foreign_keys="bountydns.db.models.api_token.ApiToken.dns_server_id",
        back_populates="dns_server",
    )

    zones = relationship(
        "bountydns.db.models.zone.Zone",
        foreign_keys="bountydns.db.models.zone.Zone.dns_server_id",
        back_populates="dns_server",
    )

    dns_requests = relationship(
        "bountydns.db.models.dns_request.DnsRequest",
        foreign_keys="bountydns.db.models.dns_request.DnsRequest.dns_server_id",
        back_populates="dns_server",
    )
