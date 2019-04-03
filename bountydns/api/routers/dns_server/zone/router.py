from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.db.models.zone import Zone
from bountydns.core.entities import (
    SortQS,
    PaginationQS,
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
    BaseResponse,
)

router = APIRouter()
options = {"prefix": "/dns-server/{dns_server_name}"}


@router.get("/zone", name="dns_server.zone.index", response_model=ZonesResponse)
async def index(
    dns_server_name: str,
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = ScopedTo("zone:list"),
):
    pg, items = (
        zone_repo.filter_or(
            Zone.dns_server_name == dns_server_name, Zone.dns_server_name.is_(None)
        )
        .sort(sort_qs)
        .paginate(pagination)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)
