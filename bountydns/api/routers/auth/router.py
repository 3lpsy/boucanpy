from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from starlette.requests import Request

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/login", name="auth.login")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    return RedirectResponse(url=request.url_for("auth.token"), status_code=307)
