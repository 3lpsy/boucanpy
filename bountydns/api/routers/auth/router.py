from fastapi import APIRouter

router = APIRouter()
options = {"prefix": "/auth"}


@router.post("/login", name="auth.login")
async def login():
    return "logging in"
