from fastapi import APIRouter, Security

from bountydns.core.security import ScopedTo, oauth2

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index")
async def index(page: int = 1, per_page: int = 20, token: str = ScopedTo("zone:list")):
    return "listing zones"


@router.get("/zone/{zone_id}", name="zone.show")
async def show(zone_id: int, token: str = ScopedTo("zone:read")):
    return "reading zones"


@router.post("/zone", name="zone.store")
async def store(token: str = ScopedTo("zone:create")):
    return "create zones"


@router.put("/zone/{zone_id}", name="zone.update")
async def update(zone_id: int, token: str = ScopedTo("zone:update")):
    return "update zones"


@router.delete("/zone/{zone_id}", name="zone.destroy")
async def destroy(zone_id: int, token: str = ScopedTo("zone:delete")):
    return "destroy zones"
