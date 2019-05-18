from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ApiToken(Base):
    __tablename__ = "api_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    scopes = Column(String)
    is_active = Column(Boolean(), default=True)
    expires_at = Column(DateTime, default=True)

    dns_server_id = Column(ForeignKey("dns_servers.id"), nullable=False)
    dns_server = relationship(
        "bountydns.db.models.dns_server.DnsServer",
        foreign_keys="bountydns.db.models.api_token.ApiToken.dns_server_id",
        back_populates="api_tokens",
    )
