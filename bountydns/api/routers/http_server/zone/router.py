from typing import List
from fastapi import APIRouter, Depends, Query
from bountydns.core import only
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.db.models.zone import Zone
from bountydns.core import SortQS, PaginationQS, BaseResponse
from bountydns.core.zone import (
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
)

router = APIRouter()
options = {"prefix": "/http-server/{http_server}"}


@router.get("/zone", name="http_server.zone.index", response_model=ZonesResponse)
async def index(
    http_server: str,
    sort_qs: SortQS = Depends(SortQS),
    search: str = Query(None),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:list")),
    includes: List[str] = Query(None),
):

    includes = only(includes, ["http_records"], values=True)

    # Support ability to either submit http_server.name or http_server.id as http_server_id
    zone_http_server_id_label = zone_repo.label("http_server_id")

    try:
        http_server = int(http_server)
        label = zone_http_server_id_label
    except ValueError:
        label = zone_repo.label("http_server.name")

    pg, items = (
        zone_repo.search(search)
        .loads(includes)
        .filter_or(label == http_server, zone_http_server_id_label.is_(None))
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)
