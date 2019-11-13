from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    email_verified = Column(Boolean, default=False)

    hashed_password = Column(String)
    mfa_secret = Column(String, nullable=True)

    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
