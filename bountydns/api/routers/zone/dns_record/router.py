from typing import List
from textwrap import dedent
from dnslib import RR
from dnslib.dns import DNSError
from fastapi import APIRouter, Depends, Query
from bountydns.core import only
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import SortQS, PaginationQS

from bountydns.core.entities.dns_record import (
    DnsRecordsResponse,
    DnsRecordResponse,
    DnsRecordRepo,
    DnsRecordForZoneCreateForm,
)
from bountydns.core.entities.zone import ZoneRepo

router = APIRouter()
options = {"prefix": "/zone/{zone_id}"}


@router.get(
    "/dns-record", name="zone.dns_record.index", response_model=DnsRecordsResponse
)
async def index(
    zone_id: int,
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("dns-record:list")),
    includes: List[str] = Query(None),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    includes = only(includes, ["zone"], values=True)

    pg, items = (
        dns_record_repo.loads("zone")
        .sort(sort_qs)
        .filter_by(zone_id=zone_id)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return DnsRecordsResponse(pagination=pg, dns_records=items)


@router.post(
    "/dns-record", name="zone.dns_record.store", response_model=DnsRecordResponse
)
async def store(
    zone_id: int,
    form: DnsRecordForZoneCreateForm,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("dns-record:create")),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    data = only(dict(form), ["record", "sort"])
    data["zone_id"] = zone_id

    # TODO: make sure sorts don't clash
    item = dns_record_repo.create(data).data()
    return DnsRecordResponse(dns_record=item)


@router.get(
    "/dns-record/{dns_record_id}",
    name="zone.dns_record.show",
    response_model=DnsRecordResponse,
)
async def show(
    zone_id: int,
    dns_record_id: int,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("dns-record:show")),
    includes: List[str] = Query(None),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    includes = only(includes, ["zone"], values=True)

    item = (
        dns_record_repo.loads("zone")
        .filter_by(zone_id=zone_id)
        .first_or_fail(id=dns_record_id)
        .includes(includes)
        .data()
    )

    return DnsRecordResponse(dns_record=item)


# TODO: create update form for dns record


@router.put(
    "/dns-record/{dns_record_id}",
    name="zone.dns_record.update",
    response_model=DnsRecordResponse,
)
async def update(
    zone_id: int,
    dns_record_id: int,
    form: DnsRecordForZoneCreateForm,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo),
    zone_repo: ZoneRepo = Depends(ZoneRepo),
    token: TokenPayload = Depends(ScopedTo("dns-record:create")),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    data = only(dict(form), ["record", "sort"])

    # TODO: make sure sorts don't clash
    item = dns_record_repo.first_or_fail(id=dns_record_id).update(data).data()
    return DnsRecordResponse(dns_record=item)
