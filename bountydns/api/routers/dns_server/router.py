from fastapi import APIRouter, Depends
from bountydns.core import logger
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import DnsServerRepo, PaginationQS, DnsServersResponse

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-server", name="dns_server.index", response_model=DnsServersResponse)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = ScopedTo("dns-request:list"),
):
    pg, items = dns_server_repo.paginate(pagination).data()
    return DnsServersResponse(pagination=pg, dns_servers=items)
