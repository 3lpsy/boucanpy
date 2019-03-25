from datetime import timedelta, datetime

from passlib.context import CryptContext
import jwt


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return context.hash(password)


def create_bearer_token(*, data: dict, expires_delta: timedelta = None):
    from bountydns.api import config  # environment must be loaded

    expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.API_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )

    return encoded_jwt
