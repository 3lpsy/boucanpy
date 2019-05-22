from fastapi import APIRouter, Depends, Query
from bountydns.core import logger, only, abort
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import (
    PaginationQS,
    SortQS,
    DnsServerRepo,
    DnsServersResponse,
    DnsServerResponse,
    DnsServerCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-server", name="dns_server.index", response_model=DnsServersResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("dns-server:list")),
    search: str = Query(None),
):
    pg, items = (
        dns_server_repo.search(search, searchable=["name", "id"])
        .paginate(pagination)
        .data()
    )
    return DnsServersResponse(pagination=pg, dns_servers=items)


@router.post("/dns-server", name="dns_server.store", response_model=DnsServerResponse)
async def store(
    form: DnsServerCreateForm,
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("dns-server:create")),
):
    if dns_server_repo.exists(name=form.name.lower()):
        abort(422, "Invalid Name")

    data = only(dict(form), ["name"])
    data["name"] = data["name"].lower()
    item = dns_server_repo.create(data).data()
    return DnsServerResponse(dns_server=item)


@router.get(
    "/dns-server/{dns_server}", name="dns_server.show", response_model=DnsServerResponse
)
async def show(
    dns_server: str,
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("dns-server:show")),
):

    dns_server_id_label = dns_server_repo.label("id")

    try:
        dns_server = int(dns_server)
        label = dns_server_id_label
    except ValueError:
        label = dns_server_repo.label("name")

    item = dns_server_repo.filter(label == dns_server).first_or_fail().data()

    return DnsServerResponse(dns_server=item)


# TODO: make specifi update form for dns server
@router.put(
    "/dns-server/{dns_server}",
    name="dns_server.update",
    response_model=DnsServerResponse,
)
async def update(
    dns_server: str,
    form: DnsServerCreateForm,
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("dns-server:update")),
):

    data = only(dict(form), ["name"])
    data["name"] = data["name"].lower()

    dns_server_id_label = dns_server_repo.label("id")

    try:
        dns_server = int(dns_server)
        label = dns_server_id_label
    except ValueError:
        label = dns_server_repo.label("name")

    item = (
        dns_server_repo.filter(label == dns_server).first_or_fail().update(data).data()
    )

    return DnsServerResponse(dns_server=item)
