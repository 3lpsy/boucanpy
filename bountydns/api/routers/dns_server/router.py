from fastapi import APIRouter, Depends, Query
from bountydns.core import logger
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import (
    PaginationQS,
    SortQS,
    DnsServerRepo,
    DnsServersResponse,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-server", name="dns_server.index", response_model=DnsServersResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("dns-request:list")),
    search: str = Query(None),
):
    pg, items = (
        dns_server_repo.search(search, searchable=["name", "id"])
        .paginate(pagination)
        .data()
    )
    return DnsServersResponse(pagination=pg, dns_servers=items)
