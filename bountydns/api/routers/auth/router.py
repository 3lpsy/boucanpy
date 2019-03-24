from fastapi import APIRouter

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/login", name="auth.login")
async def login():
    return "logging in"


@router.post("/login/mfa", name="auth.mfa.login")
async def mfa_login():
    return "logging in"
