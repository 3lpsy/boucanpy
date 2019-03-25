from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bountydns.core.entities.auth import PasswordAuthForm, PasswordAuthResponse
from bountydns.core.security import verify_password, create_bearer_token
from bountydns.db.models.user import User
from bountydns.db.session import resolve_db

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/login", name="auth.login", response_model=PasswordAuthResponse)
async def login(form: PasswordAuthForm, db: Session = Depends(resolve_db("api"))):
    user = db.query(User).filter_by(email=form.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if user.mfa_secret:  # mfa is enabled
        scopes = "profile password_enabled password_authenticated mfa_enabled"
    else:
        scopes = "profile password_enabled password_authenticated"

    token = create_bearer_token(data={"sub": user.id, "scopes": scopes})
    return PasswordAuthResponse(token_type="bearer", access_token=str(token.decode()))
