from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from bountydns.core import logger
from bountydns.core.entities.auth import PasswordAuthResponse
from bountydns.core.security import verify_password, create_bearer_token
from bountydns.db.models.user import User
from bountydns.db.session import session

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/token", name="auth.token", response_model=PasswordAuthResponse)
async def login(
    db: Session = Depends(session), form: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter_by(email=form.username).first()
    if not user or not user.hashed_password:
        logger.warning(f"user exists failed for {form.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(form.password, user.hashed_password):
        logger.warning(f"hash verification failed for {form.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if user.mfa_secret:  # mfa is enabled
        scopes = "profile mfa_required"
    elif user.is_superuser:
        scopes = (
            "profile super zone user dns-request api-token"
        )  # grant access to super routes
    else:
        scopes = "profile zone user:list dns-request api-token:list api-token:create api-token:destroy"
    logger.warning(f"creating token with scopes {scopes}")
    token = create_bearer_token(data={"sub": user.id, "scopes": scopes})
    return PasswordAuthResponse(token_type="bearer", access_token=str(token.decode()))
