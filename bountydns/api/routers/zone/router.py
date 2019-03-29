from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo
from bountydns.core.entities import ZoneRepo, PaginationQS, ZonesResponse, ZoneData

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index", response_model=ZonesResponse)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: str = ScopedTo("zone:list"),
):
    pg, items = zone_repo.paginate(pagination).set_data_model(ZoneData).data()
    return ZonesResponse(pagination=pg, zones=items)
