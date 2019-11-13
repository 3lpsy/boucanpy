from fastapi import APIRouter, Depends, Query
from typing import List
from boucanpy.core.security import ScopedTo, TokenPayload
from boucanpy.core import logger, only, abort, abort_for_input

from boucanpy.core import SortQS, PaginationQS, BaseResponse
from boucanpy.core.dns_server import DnsServerRepo
from boucanpy.core.http_server import HttpServerRepo

from boucanpy.core.zone import (
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index", response_model=ZonesResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:list")),
    includes: List[str] = Query(None),
):
    # TODO: bypasses a bunch of scopes, find a way to restrict access via scopes
    includes = only(includes, ["dns_server", "dns_records", "http_server"], values=True)

    pg, items = (
        zone_repo.loads(includes)
        .strict()
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)


@router.post("/zone", name="zone.store", response_model=ZoneResponse)
async def store(
    form: ZoneCreateForm,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:create")),
):

    data = only(dict(form), ["ip", "domain"])

    data["domain"] = data["domain"].lower()

    # Make sure domain is unique

    if zone_repo.exists(domain=data["domain"]):
        abort_for_input("domain", "A Zone with that domain already exists")

    zone_repo.clear()

    if form.dns_server_id:
        if dns_server_repo.exists(id=form.dns_server_id):
            data["dns_server_id"] = dns_server_repo.results().id

    if form.http_server_id:
        if http_server_repo.exists(id=form.http_server_id):
            data["http_server_id"] = http_server_repo.results().id

    zone = zone_repo.create(data).data()
    return ZoneResponse(zone=zone)


@router.get("/zone/{zone_id}", name="zone.show", response_model=ZoneResponse)
async def show(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:show")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["dns_server", "dns_records", "http_server"], values=True)

    zone = zone_repo.loads(includes).get_or_fail(zone_id).includes(includes).data()
    return ZoneResponse(zone=zone)


# TODO: make custom update form for zone
@router.put("/zone/{zone_id}", name="zone.update", response_model=ZoneResponse)
async def update(
    zone_id: int,
    form: ZoneCreateForm,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    http_server_repo: DnsServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
    includes: List[str] = Query(None),
):
    data = only(dict(form), ["ip", "domain"])

    if "domain" in data:
        data["domain"] = data["domain"].lower()
        existing_domain = zone_repo.first(domain=data["domain"]).results()
        if existing_domain and existing_domain.id != zone_id:
            abort_for_input("domain", "A Zone with that domain already exists")
        zone_repo.clear()

    if form.dns_server_id is not None:
        if form.dns_server_id is 0:
            data["dns_server_id"] = None
        elif dns_server_repo.exists(id=form.dns_server_id):
            dns_server = dns_server_repo.results()
            data["dns_server"] = dns_server

    if form.http_server_id is not None:
        if form.http_server_id is 0:
            data["http_server_id"] = None
        elif http_server_repo.exists(id=form.http_server_id):
            http_server = http_server_repo.results()
            data["http_server"] = http_server

    zone = (
        zone_repo.loads(includes)
        .get_or_fail(zone_id)
        .update(data)
        .includes(includes)
        .data()
    )
    return ZoneResponse(zone=zone)


@router.put(
    "/zone/{zone_id}/activate", name="zone.activate", response_model=ZoneResponse
)
async def activate(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
):
    zone = zone_repo.get_or_fail(zone_id).update({"is_active": True}).data()
    return ZoneResponse(zone=zone)


@router.delete("/zone/{zone_id}", name="zone.destroy", response_model=BaseResponse)
async def destroy(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:destroy")),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not zone_repo.exists(zone_id):
        return BaseResponse(messages=messages)
    zone_repo.deactivate(zone_id)
    return BaseResponse(messages=messages)
