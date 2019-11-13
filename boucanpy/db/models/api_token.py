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

    dns_server_id = Column(ForeignKey("dns_servers.id"), nullable=True)
    dns_server = relationship(
        "boucanpy.db.models.dns_server.DnsServer",
        foreign_keys="boucanpy.db.models.api_token.ApiToken.dns_server_id",
        back_populates="api_tokens",
    )

    http_server_id = Column(ForeignKey("http_servers.id"), nullable=True)
    http_server = relationship(
        "boucanpy.db.models.http_server.HttpServer",
        foreign_keys="boucanpy.db.models.api_token.ApiToken.http_server_id",
        back_populates="api_tokens",
    )
