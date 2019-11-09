from sqlalchemy import literal
from fastapi import APIRouter, Depends, Query
from typing import List

from bountydns.core import logger, abort, only
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core import SortQS, PaginationQS
from bountydns.core.http_server import HttpServerRepo
from bountydns.core.zone import ZoneRepo

from bountydns.core.http_request import (
    HttpRequestRepo,
    HttpRequestsResponse,
    HttpRequestResponse,
    HttpRequestData,
    HttpRequestCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get(
    "/http-request", name="http_request.index", response_model=HttpRequestsResponse
)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    http_request_repo: HttpRequestRepo = Depends(HttpRequestRepo()),
    token: TokenPayload = Depends(ScopedTo("http-request:list")),
):
    pg, items = (
        http_request_repo.loads("http_server")
        .sort(sort_qs)
        .includes("http_server")
        .paginate(pagination)
        .data()
    )
    return HttpRequestsResponse(pagination=pg, http_requests=items)


@router.post(
    "/http-request", name="http_request.store", response_model=HttpRequestResponse
)
async def store(
    form: HttpRequestCreateForm,
    http_request_repo: HttpRequestRepo = Depends(HttpRequestRepo()),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: str = Depends(ScopedTo("http-request:create")),
):

    http_server_id = (
        http_server_repo.first_or_fail(name=form.http_server_name.lower()).results().id
    )

    zone = (
        zone_repo.filter(literal(form.name.lower()).contains(zone_repo.label("domain")))
        .first()
        .results()
    )

    zone_id = zone.id if zone else None

    data = only(
        dict(form),
        [
            "name",
            "path",
            "source_address",
            "source_port",
            "type",
            "protocol",
            "raw_request",
        ],
    )

    data["name"] = data["name"].lower()
    data["type"] = data["type"].upper()

    data["http_server_id"] = http_server_id
    data["zone_id"] = zone_id
    logger.info("store@router.py - Creating HTTP Request")
    http_request = http_request_repo.create(data).data()

    return HttpRequestResponse(http_request=http_request)


@router.get(
    "/http-request/{http_request_id}",
    name="http_request.show",
    response_model=HttpRequestResponse,
)
async def show(
    http_request_id: int,
    http_request_repo: HttpRequestRepo = Depends(HttpRequestRepo()),
    token: TokenPayload = Depends(ScopedTo("http-request:show")),
    includes: List[str] = Query(None),
):
    # probably a bunch of access bypasses with scopes via includes
    # need easy way to scope for includes
    includes = only(includes, ["http_server", "zone"], values=True)

    http_request = (
        http_request_repo.loads(includes)
        .get_or_fail(http_request_id)
        .includes(includes)
        .data()
    )
    return HttpRequestResponse(http_request=http_request)
