from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from bountydns.core import logger
from bountydns.core.auth import PasswordAuthResponse
from bountydns.core.security import verify_password, create_bearer_token
from bountydns.db.models.user import User
from bountydns.db.session import session

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/token", name="auth.token", response_model=PasswordAuthResponse)
async def login(
    ws_access_token: bool = False,
    db: Session = Depends(session),
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
        scopes = "profile super zone user dns-request api-token refresh dns-record dns-server"  # grant access to super routes
    else:
        scopes = "profile zone user:list dns-request api-token:list api-token:create api-token:destroy refresh dns-record:list dns-record:show dns-server:list dns-server:show"

    logger.warning(f"creating token with scopes {scopes}")

    token = create_bearer_token(data={"sub": user.id, "scopes": scopes})
    data = {"token_type": "bearer", "access_token": str(token.decode())}

    if ws_access_token:
        # TODO: make it so that you cannot get publish access without base scope
        data["ws_access_token"] = create_bearer_token(
            data={"sub": user.id, "scopes": "zone:publish dns-request:publish refresh"}
        )
    return PasswordAuthResponse(**data)
