from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from bountydns.core import logger, only, abort
from bountydns.core.security import (
    ScopedTo,
    TokenPayload,
    create_bearer_token,
    current_user,
)
from bountydns.db.models.user import User
from bountydns.db.models.dns_server import DnsServer
from bountydns.db.models.http_server import HttpServer

from bountydns.core.api_token import (
    ApiTokensResponse,
    ApiTokenResponse,
    ApiTokenRepo,
    ApiTokenCreateForm,
    ApiTokenData,
    SensitiveApiTokenResponse,
    SensitiveApiTokenData,
)
from bountydns.core.dns_server import DnsServerRepo
from bountydns.core.http_server import HttpServerRepo

from bountydns.core import SortQS, PaginationQS, BaseResponse


router = APIRouter()
options = {"prefix": ""}


# TODO: fix this
@router.post("/api-token/sync", name="api_token.sync", response_model=ApiTokenResponse)
async def sync(
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo()),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("api-token:syncable")),
):
    if "api-token" in token.scopes or "api-token:syncable" in token.scopes:
        abort_for_no_server_names(token)
        if (
            len(token.payload.dns_server_name) > 0
            and len(token.payload.http_server_name) > 0
        ):
            dns_server = create_or_get_dns_server(token, dns_server_repo)
            http_server = create_or_get_http_server(token, http_server_repo)
            api_token_data = create_or_get_api_token_for_all_nodes(
                token, api_token_repo, dns_server, http_server
            )
        elif len(token.payload.dns_server_name) > 0:
            dns_server = create_or_get_dns_server(token, dns_server_repo)
            api_token_data = create_or_get_api_token_for_dns_server(
                token, api_token_repo, dns_server
            )

        elif len(token.payload.http_server_name) > 0:
            http_server = create_or_get_http_server(token, http_server_repo)
            api_token_data = create_or_get_api_token_for_http_server(
                token, api_token_repo, http_server
            )
        else:
            # something went wrong, should not hit
            raise HTTPException(403, detail="Not found")

        return ApiTokenResponse(api_token=api_token_data)

    else:
        raise HTTPException(403, detail="Not found")


@router.get("/api-token", name="api_token.index", response_model=ApiTokensResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo()),
    token: TokenPayload = Depends(ScopedTo("api-token:list")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["dns_server", "http_server"], values=True)

    pg, items = (
        api_token_repo.loads(includes)
        .strict()
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return ApiTokensResponse(pagination=pg, api_tokens=items)


@router.post("/api-token", name="api_token.store", response_model=ApiTokenResponse)
async def store(
    form: ApiTokenCreateForm,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo()),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("api-token:create")),
    user: User = Depends(current_user),
):
    if form.dns_server_id and form.dns_server_id > 0:
        dns_server_name = (
            dns_server_repo.first_or_fail(id=form.dns_server_id).results().name
        )
    if form.http_server_id and form.http_server_id > 0:
        http_server_name = (
            http_server_repo.first_or_fail(id=form.http_server_id).results().name
        )
    scopes = []
    for requested_scope in form.scopes.split(" "):
        request_scope_satisfied = False
        for user_token in token.scopes:
            # TODO: double check this, pretty lenient
            # if a:b in a:b:c
            if user_token in requested_scope:
                request_scope_satisfied = True
        if not request_scope_satisfied:
            logger.warning(
                f"store@router.py: Attempt to create unauthorized scope {requested_scope}"
            )
            raise HTTPException(403, detail="unauthorized")
        else:
            scopes.append(requested_scope)

    # TODO: use better randomness

    token = create_bearer_token(
        data={
            "sub": user.id,
            "scopes": " ".join(scopes),
            "dns_server_name": dns_server_name,
            "http_server_name": http_server_name,
        }
    )

    data = {
        "scopes": " ".join(scopes),
        "token": str(token),
        "expires_at": form.expires_at,
        "dns_server_id": form.dns_server_id,
        "http_server_id": form.http_server_id,
    }

    api_token = api_token_repo.create(data).data()
    return ApiTokenResponse(api_token=api_token)


@router.get(
    "/api-token/{api_token_id}", name="api_token.show", response_model=ApiTokenResponse
)
async def show(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo()),
    token: TokenPayload = Depends(ScopedTo("api-token:read")),
    includes: List[str] = Query(None),
):

    includes = only(includes, ["dns_server", "http_server"], values=True)

    if (
        not api_token_repo.loads(includes)
        .strict()
        .includes(includes)
        .exists(api_token_id)
    ):
        raise HTTPException(404, detail="Not found")
    api_token = api_token_repo.data()
    return ApiTokenResponse(api_token=api_token)


@router.get(
    "/api-token/{api_token_id}/sensitive",
    name="api_token.show.sensitive",
    response_model=SensitiveApiTokenResponse,
)
async def sensitive(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo()),
    token: TokenPayload = Depends(ScopedTo("api-token:read")),
    includes: List[str] = Query(None),
):

    includes = only(includes, ["dns_server", "http_server"], values=True)

    # TODO: require stronger scope
    if not api_token_repo.exists(api_token_id):
        raise HTTPException(404, detail="Not found")
    api_token = (
        api_token_repo.loads(includes)
        .set_data_model(SensitiveApiTokenData)
        .includes(includes)
        .data()
    )
    return SensitiveApiTokenResponse(api_token=api_token)


@router.delete("/api-token/{api_token_id}", response_model=BaseResponse)
async def destroy(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo()),
    token: TokenPayload = Depends(ScopedTo("api-token:destroy")),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not api_token_repo.exists(api_token_id):
        return BaseResponse(messages=messages)
    api_token_repo.deactivate(api_token_id)
    return BaseResponse(messages=messages)


def abort_for_no_server_names(token: TokenPayload):
    if not len(token.payload.dns_server_name) or not len(
        token.payload.http_server_name
    ):
        abort(
            code=422, msg="No DNS Server Name or HTTP Server Name on payload", debug="",
        )


def create_or_get_api_token_for_all_nodes(
    token: TokenPayload,
    api_token_repo: ApiTokenRepo,
    dns_server: DnsServer,
    http_server: HttpServer,
) -> ApiTokenData:
    scopes = token.scopes

    if not api_token_repo.exists(token=token.token):
        api_token_repo.clear()
        logger.info("sync@router.py - Saving api token from auth token for all nodes")
        return api_token_repo.create(
            dict(
                token=token.token,
                scopes=" ".join(scopes),
                dns_server_id=dns_server.id,
                http_server_id=http_server.id,
                expires_at=datetime.utcfromtimestamp(float(token.exp)),
            )
        ).data()
    else:
        logger.info("sync@router.py - token already exists in database")
        return api_token_repo.data()


def create_or_get_dns_server(
    token: TokenPayload, dns_server_repo: DnsServerRepo
) -> DnsServer:
    if not dns_server_repo.exists(name=token.payload.dns_server_name.lower()):
        dns_server_repo.clear()
        logger.info("sync@router.py - Saving dns server from api token")
        return dns_server_repo.create(
            dict(name=token.payload.dns_server_name.lower())
        ).results()
    else:
        return dns_server_repo.results()


def create_or_get_api_token_for_dns_server(
    token: TokenPayload, api_token_repo: ApiTokenRepo, dns_server: DnsServer
) -> ApiTokenData:
    scopes = token.scopes

    if not api_token_repo.exists(token=token.token):
        api_token_repo.clear()
        logger.info("sync@router.py - Saving api token from auth token for dns node")
        return api_token_repo.create(
            dict(
                token=token.token,
                scopes=" ".join(scopes),
                dns_server=dns_server,
                expires_at=datetime.utcfromtimestamp(float(token.exp)),
            )
        ).data()
    else:
        logger.info("sync@router.py - token already exists in database")
        return api_token_repo.loads("dns_server").includes("dns_server").data()


def create_or_get_http_server(
    token: TokenPayload, http_server_repo: HttpServerRepo
) -> HttpServer:
    if not http_server_repo.exists(name=token.payload.http_server_name.lower()):
        http_server_repo.clear()
        logger.info("sync@router.py - Saving http server from api token")
        return http_server_repo.create(
            dict(name=token.payload.http_server_name.lower())
        ).results()
    else:
        return http_server_repo.results()


def create_or_get_api_token_for_http_server(
    token: TokenPayload, api_token_repo: ApiTokenRepo, http_server: HttpServer
) -> ApiTokenData:
    scopes = token.scopes

    if not api_token_repo.exists(token=token.token):
        api_token_repo.clear()
        logger.info("sync@router.py - Saving api token from auth token for http node")
        return api_token_repo.create(
            dict(
                token=token.token,
                scopes=" ".join(scopes),
                http_server=http_server,
                expires_at=datetime.utcfromtimestamp(float(token.exp)),
            )
        ).data()
    else:
        logger.info("sync@router.py - token already exists in database")
        return api_token_repo.loads("http_server").includes("http_server").data()

