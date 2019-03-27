from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from bountydns.core.entities.auth import PasswordAuthForm, PasswordAuthResponse
from bountydns.core.security import verify_password, create_bearer_token
from bountydns.db.models.user import User
from bountydns.db.session import resolve_db
from starlette.responses import RedirectResponse
from starlette.requests import Request

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/login", name="auth.login")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    return RedirectResponse(url=request.url_for("auth.token"), status_code=307)
