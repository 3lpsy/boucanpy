from fastapi import APIRouter

router = APIRouter()
options = {"prefix": "/auth/mfa"}


@router.post("/login", name="auth.mfa.login")
async def mfa_login():
    return "logging in"
