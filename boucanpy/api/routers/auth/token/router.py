from os import environ
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from boucanpy.core import logger
from boucanpy.core.auth import PasswordAuthResponse
from boucanpy.core.security import verify_password, create_bearer_token
from boucanpy.db.models.user import User
from boucanpy.db.session import async_session
from boucanpy.core.enums import SUPER_SCOPES, NORMAL_SCOPES, PUBLISH_SCOPES

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/token", name="auth.token", response_model=PasswordAuthResponse)
async def login(
    ws_access_token: bool = False,
    db: Session = Depends(async_session),
    form: OAuth2PasswordRequestForm = Depends(),
):
    username = form.username.lower() if form.username else ""

    user = db.query(User).filter_by(email=username).first()

    if not user or not user.hashed_password:
        logger.warning(f"user exists failed for {username}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not verify_password(form.password, user.hashed_password):
        logger.warning(f"hash verification failed for {username}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if user.mfa_secret:  # mfa is enabled
        scopes = "profile mfa_required"
    elif user.is_superuser:
        scopes = SUPER_SCOPES  # grant access to super routes
    else:
        scopes = NORMAL_SCOPES

    logger.warning(f"creating token with scopes {scopes}")

    token = create_bearer_token(data={"sub": user.id, "scopes": scopes})
    data = {"token_type": "bearer", "access_token": str(token)}

    if ws_access_token and int(environ.get("BROADCAST_ENABLED", 0)) == 1:
        # TODO: make it so that you cannot get publish access without base scope
        data["ws_access_token"] = create_bearer_token(
            data={"sub": user.id, "scopes": PUBLISH_SCOPES}
        )
    return PasswordAuthResponse(**data)
