from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

base_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
# base_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
#
# def get_oauth()
# def resolve_oauth()
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


# async def get_current_user(token: str = Security(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except PyJWTError:
#         raise HTTPException(
#             status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#         )
#     user = get_user(fake_users_db, username=token_data.username)
#     return user
