from datetime import timedelta, datetime
from typing import List
import jwt
from starlette.requests import Request
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from bountydns.core import logger
from bountydns.core.entities import TokenPayload, UserRepo, BlackListedTokenRepo
from bountydns.db.models.user import User

DEFAULT_TOKEN_URL = "/api/v1/auth/token"
oauth2 = OAuth2PasswordBearer(tokenUrl=DEFAULT_TOKEN_URL)


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return context.hash(password)


def create_bearer_token(
    *, data: dict, expires_delta: timedelta = None, expire: datetime = None
):
    from bountydns.api import config  # environment must be loaded

    if not expires_delta:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if not expire:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.API_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_jwt_token(token: str, bl_token_repo=None, leeway=0) -> TokenPayload:
    from bountydns.api import config  # environment must be loaded

    if bl_token_repo:
        if bl_token_repo.exists(token=token):
            raise HTTPException(status_code=403, detail="Forbidden")
    else:
        logger.warning("verifying token without checking the blacklist. dangerous!")
    try:
        payload = jwt.decode(
            token, config.API_SECRET_KEY, algorithms=config.JWT_ALGORITHM, leeway=leeway
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Forbidden")

    return TokenPayload(
        payload=payload,
        scopes=payload.get("scopes", "").split(" "),
        token=token,
        sub=payload.get("sub", ""),
        exp=payload.get("exp", ""),
    )


def token_has_required_scopes(token_payload: TokenPayload, scopes: List[str]):
    token_scopes = token_payload.scopes
    required_scopes = scopes or []
    for required_scope in required_scopes:
        satisfied = False
        for token_scope in token_scopes:
            if token_scope == required_scope:
                satisfied = True
            # probably bad / too generous
            # a:b in a:b:c
            elif token_scope in required_scope:
                satisfied = True
        if not satisfied:
            logger.critical(f"auth token missing scope: {required_scope}")

            return False
    return True


class ScopedTo(Depends):
    def __init__(self, *scopes, leeway=0) -> None:
        super().__init__(self.__call__)
        self._scopes = scopes
        self._leeway = leeway

    def __call__(
        self,
        request: Request,
        bl_token_repo: BlackListedTokenRepo = Depends(BlackListedTokenRepo),
        token: str = Security(oauth2),
    ) -> TokenPayload:
        token = verify_jwt_token(
            token, bl_token_repo, self._leeway
        )  # proper validation goes here
        if not token_has_required_scopes(token, self._scopes):
            raise HTTPException(403, detail="Forbidden")
        return token


def current_user(
    token: TokenPayload = ScopedTo(), user_repo: UserRepo = Depends(UserRepo)
) -> User:
    user = user_repo.get_by_sub(token.sub)
    if not user:
        raise HTTPException(404, detail="Not Found")
    return user
