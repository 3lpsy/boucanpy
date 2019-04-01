from fastapi import APIRouter, Depends
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import (
    ZoneRepo,
    PaginationQS,
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
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = ScopedTo("zone:list"),
):
    pg, items = zone_repo.paginate(pagination).set_data_model(ZoneData).data()
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
