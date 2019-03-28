from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo
from bountydns.core.entities import ZoneRepo, PaginationQS, ZonesResponse

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index", response_model=ZonesResponse)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: str = ScopedTo("zone:list"),
):
    pg, items = zone_repo.paginate(pagination)
    return ZonesResponse(pagination=pg, zones=items)
