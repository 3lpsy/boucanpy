from fastapi import APIRouter

router = APIRouter()
options = {"prefix": ""}


@router.get("/status", name="status.show")
async def login():
    return {"status": "up"}
