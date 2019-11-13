from typing import List
from fastapi import APIRouter, Depends, Query
from boucanpy.core import only
from boucanpy.core.security import ScopedTo, TokenPayload
from boucanpy.db.models.zone import Zone
from boucanpy.core import SortQS, PaginationQS, BaseResponse
from boucanpy.core.zone import (
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
)

router = APIRouter()
options = {"prefix": "/dns-server/{dns_server}"}


@router.get("/zone", name="dns_server.zone.index", response_model=ZonesResponse)
async def index(
    dns_server: str,
    sort_qs: SortQS = Depends(SortQS),
    search: str = Query(None),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:list")),
    includes: List[str] = Query(None),
):

    includes = only(includes, ["dns_records"], values=True)

    # Support ability to either submit dns_server.name or dns_server.id as dns_server_id
    zone_dns_server_id_label = zone_repo.label("dns_server_id")

    try:
        dns_server = int(dns_server)
        label = zone_dns_server_id_label
    except ValueError:
        label = zone_repo.label("dns_server.name")

    pg, items = (
        zone_repo.search(search)
        .loads(includes)
        .filter_or(label == dns_server, zone_dns_server_id_label.is_(None))
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)
