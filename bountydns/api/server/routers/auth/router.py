from fastapi import APIRouter

router = APIRouter()
options = {"prefix": "/auth"}


@router.get("/login")
async def login():
    return "logging in"
