from fastapi import APIRouter

router = APIRouter()
options = {"prefix": ""}


@router.get("/status", name="staus.show")
async def login():
    return {"status": "up"}
