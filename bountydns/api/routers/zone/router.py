from fastapi import APIRouter

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index")
async def index():
    return "logging in"


@router.get("/zone/{zone_id}", name="zone.show")
async def show():
    return "logging in"


@router.post("/zone", name="zone.store")
async def store():
    return "logging in"


@router.put("/zone/{zone_id}", name="zone.update")
async def update():
    return "logging in"


@router.delete("/zone/{zone_id}", name="zone.destroy")
async def destroy():
    return "logging in"
