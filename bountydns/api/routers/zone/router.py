from fastapi import APIRouter, Depends, Query
from typing import List
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core import logger, only

from bountydns.core.entities import (
    SortQS,
    PaginationQS,
    DnsServerRepo,
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
    BaseResponse,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index", response_model=ZonesResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("zone:list")),
    includes: List[str] = Query(None),
):
    pg, items = (
        zone_repo.loads("dns_server")
        .strict()  # TODO: handle eagerloading when including
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)


@router.post("/zone", name="zone.store", response_model=ZoneResponse)
async def store(
    form: ZoneCreateForm,
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("zone:create")),
):
    data = only(dict(form), ["ip", "domain"])
    if form.dns_server_id:
        if dns_server_repo.exists(id=form.dns_server_id):
            dns_server = dns_server_repo.results()
            data["dns_server"] = dns_server
    zone = zone_repo.create(data).data()
    return ZoneResponse(zone=zone)


@router.get("/zone/{zone_id}", name="zone.show", response_model=ZoneResponse)
async def show(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
    includes: List[str] = Query(None),
):
    zone = zone_repo.loads("dns_server").get_or_fail(zone_id).includes(includes).data()
    return ZoneResponse(zone=zone)


# TODO: make custom update form for zone
@router.put("/zone/{zone_id}", name="zone.update", response_model=ZoneResponse)
async def show(
    zone_id: int,
    form: ZoneCreateForm,
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
    includes: List[str] = Query(None),
):
    data = only(dict(form), ["ip", "domain"])
    if form.dns_server_id is not None:
        if form.dns_server_id is 0:
            data["dns_server_id"] = None
        elif dns_server_repo.exists(id=form.dns_server_id):
            dns_server = dns_server_repo.results()
            data["dns_server"] = dns_server

    zone = (
        zone_repo.loads("dns_server")
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
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
):
    zone = zone_repo.get(zone_id).update({"is_active": True}).data()
    return ZoneResponse(zone=zone)


@router.delete("/zone/{zone_id}", response_model=BaseResponse)
async def destroy(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("zone:destroy")),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not zone_repo.exists(zone_id):
        return BaseResponse(messages=messages)
    zone_repo.deactivate(zone_id)
    return BaseResponse(messages=messages)
