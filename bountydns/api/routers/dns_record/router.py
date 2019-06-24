from fastapi import APIRouter, Depends, Query
from typing import List
from starlette.responses import RedirectResponse
from starlette.requests import Request
from bountydns.core import only, logger
from bountydns.core.security import ScopedTo, TokenPayload

from bountydns.core.dns_record import (
    DnsRecordsResponse,
    DnsRecordResponse,
    DnsRecordRepo,
    DnsRecordForZoneCreateForm,
)

from bountydns.core import SortQS, PaginationQS, BaseResponse

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-record", name="dns_record.index", response_model=DnsRecordsResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:list")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zone"], values=True)

    pg, items = (
        dns_record_repo.loads("zone")
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )

    return DnsRecordsResponse(pagination=pg, dns_records=items)


@router.post("/dns-record", name="dns_record.store")
async def store(request: Request, form: DnsRecordForZoneCreateForm = Depends()):
    return RedirectResponse(
        url=request.url_for("zone.dns_record.store", zone_id=form.zone_id),
        status_code=307,
    )


@router.get(
    "/dns-record/{dns_record_id}",
    name="dns_record.show",
    response_model=DnsRecordResponse,
)
async def show(
    dns_record_id: int,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:show")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zone"], values=True)

    item = (
        dns_record_repo.loads("zone")
        .first_or_fail(id=dns_record_id)
        .includes(includes)
        .data()
    )

    return DnsRecordResponse(dns_record=item)


# TODO: create update form for dns record
@router.put("/dns-record/{dns_record_id}", name="dns_record.update")
async def update(
    dns_record_id: int, request: Request, form: DnsRecordForZoneCreateForm = Depends()
):
    return RedirectResponse(
        url=request.url_for(
            "zone.dns_record.update", zone_id=form.zone_id, dns_record_id=dns_record_id
        ),
        status_code=307,
    )


@router.delete(
    "/dns-record/{dns_record_id}",
    name="dns_record.destroy",
    response_model=BaseResponse,
)
async def destroy(
    dns_record_id: int,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:destroy")),
):

    dns_record_repo.first_or_fail(id=dns_record_id).delete()
    messages = [{"text": "Delete Succesful", "type": "success"}]
    return BaseResponse(messages=messages)
