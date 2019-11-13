from sqlalchemy import Boolean, Column, Integer, String, DateTime

from .base import Base


class BlackListedToken(Base):
    __tablename__ = "black_listed_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
