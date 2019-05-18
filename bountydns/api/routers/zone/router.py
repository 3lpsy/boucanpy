from fastapi import APIRouter, Depends, Query
from typing import List
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core import logger

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
options = {"prefix": ""}


@router.get("/zone", name="zone.index", response_model=ZonesResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = ScopedTo("zone:list"),
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
    token: TokenPayload = ScopedTo("zone:create"),
):

    zone = zone_repo.create(form).data()
    return ZoneResponse(zone=zone)


@router.put(
    "/zone/{zone_id}/activate", name="zone.activate", response_model=ZoneResponse
)
async def activate(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = ScopedTo("zone:update"),
):
    zone = zone_repo.get(zone_id).update({"is_active": True}).data()
    return ZoneResponse(zone=zone)


@router.delete("/zone/{zone_id}", response_model=BaseResponse)
async def destroy(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = ScopedTo("zone:destroy"),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not zone_repo.exists(zone_id):
        return BaseResponse(messages=messages)
    zone_repo.deactivate(zone_id)
    return BaseResponse(messages=messages)
