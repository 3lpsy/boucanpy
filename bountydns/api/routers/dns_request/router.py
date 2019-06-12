from sqlalchemy import literal
from fastapi import APIRouter, Depends
from bountydns.core import logger, abort, only
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core import SortQS, PaginationQS
from bountydns.core.dns_server import DnsServerRepo
from bountydns.core.zone import ZoneRepo

from bountydns.core.dns_request import (
    DnsRequestRepo,
    DnsRequestsResponse,
    DnsRequestResponse,
    DnsRequestData,
    DnsRequestCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get(
    "/dns-request", name="dns_request.index", response_model=DnsRequestsResponse
)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_request_repo: DnsRequestRepo = Depends(DnsRequestRepo),
    token: TokenPayload = Depends(ScopedTo("dns-request:list")),
):
    pg, items = (
        dns_request_repo.loads("dns_server")
        .sort(sort_qs)
        .paginate(pagination)
        .includes("dns_server")
        .data()
    )
    return DnsRequestsResponse(pagination=pg, dns_requests=items)


@router.post(
    "/dns-request", name="dns_request.store", response_model=DnsRequestResponse
)
async def store(
    form: DnsRequestCreateForm,
    dns_request_repo: DnsRequestRepo = Depends(DnsRequestRepo),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: str = Depends(ScopedTo("dns-request:create")),
):

    dns_server_id = (
        dns_server_repo.first_or_fail(name=form.dns_server_name.lower()).results().id
    )

    zone = (
        zone_repo.filter(literal(form.name.lower()).contains(zone_repo.label("domain")))
        .first()
        .results()
    )

    zone_id = zone.id if zone else None

    data = only(
        dict(form), ["name", "source_address", "source_port", "type", "protocol"]
    )

    data["name"] = data["name"].lower()
    data["type"] = data["type"].upper()

    data["dns_server_id"] = dns_server_id
    data["zone_id"] = zone_id

    dns_request = dns_request_repo.create(data).data()
    return DnsRequestResponse(dns_request=dns_request)
