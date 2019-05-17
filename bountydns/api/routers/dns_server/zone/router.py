from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.db.models.zone import Zone
from bountydns.core.entities import (
    SortQS,
    PaginationQS,
    SearchQS,
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
    BaseResponse,
)

router = APIRouter()
options = {"prefix": "/dns-server/{dns_server_id}"}


@router.get("/zone", name="dns_server.zone.index", response_model=ZonesResponse)
async def index(
    dns_server_id: str,
    sort_qs: SortQS = Depends(SortQS),
    search_qs: SearchQS = Depends(SearchQS),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = ScopedTo("zone:list"),
):

    # Support ability to either submit dns_server.name or dns_server.id as dns_server_id
    zone_dns_server_id_label = zone_repo.label("dns_server_id")
    try:
        dns_server_id = int(dns_server_id)
        label = zone_dns_server_id_label
    except ValueError:
        label = zone_repo.label("dns_server.name")

    pg, items = (
        zone_repo.search(search_qs)
        .filter_or(label == dns_server_id, zone_dns_server_id_label.is_(None))
        .sort(sort_qs)
        .paginate(pagination)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)
