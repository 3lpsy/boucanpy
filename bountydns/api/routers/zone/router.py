from fastapi import APIRouter, Security

from bountydns.core.security import oauth2_scheme

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index")
async def index(
    page: int = 1,
    per_page: int = 20,
    token: str = Security(oauth2_scheme, scopes=["dns"]),
):
    return "logging in"


@router.get("/zone/{zone_id}", name="zone.show")
async def show(zone_id: int, token: str = Security(oauth2_scheme, scopes=["dns"])):
    return "logging in"


@router.post("/zone", name="zone.store")
async def store(token: str = Security(oauth2_scheme, scopes=["dns"])):
    return "logging in"


@router.put("/zone/{zone_id}", name="zone.update")
async def update(zone_id: int, token: str = Security(oauth2_scheme, scopes=["dns"])):
    return "logging in"


@router.delete("/zone/{zone_id}", name="zone.destroy")
async def destroy(zone_id: int, token: str = Security(oauth2_scheme, scopes=["dns"])):
    return "logging in"
