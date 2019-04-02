from sqlalchemy import Boolean, Column, Integer, String, DateTime

from .base import Base


class ApiToken(Base):
    __tablename__ = "api_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    scopes = Column(String)
    is_active = Column(Boolean(), default=True)
    expires_at = Column(DateTime, default=True)
    dns_server_name = Column(String)
