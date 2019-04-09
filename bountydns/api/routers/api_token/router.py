from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from bountydns.core import logger, only
from bountydns.core.security import (
    ScopedTo,
    TokenPayload,
    create_bearer_token,
    current_user,
)
from bountydns.db.models.user import User
from bountydns.core.entities import (
    SortQS,
    PaginationQS,
    ApiTokensResponse,
    ApiTokenResponse,
    ApiTokenRepo,
    ApiTokenCreateForm,
    SensitiveApiTokenResponse,
    SensitiveApiTokenData,
    BaseResponse,
)


router = APIRouter()
options = {"prefix": ""}


@router.post("/api-token/sync", name="api_token.sync", response_model=ApiTokenResponse)
async def index(
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:syncable"),
):
    scopes = token.scopes
    if "api-token" in scopes or "api-token:syncable" in scopes:
        api_token = None
        if not api_token_repo.exists(token=token.token):
            api_token_repo.clear()
            logger.info("saving api token from auth token")
            api_token = api_token_repo.create(
                dict(
                    token=token.token,
                    scopes=" ".join(scopes),
                    dns_server_name=token.payload.dns_server_name,
                    expires_at=datetime.utcfromtimestamp(float(token.exp)),
                )
            ).data()
        else:
            logger.info("token already exists in database")
            api_token = api_token_repo.data()
        return ApiTokenResponse(api_token=api_token)

    else:
        raise HTTPException(403, detail="Not found")


@router.get("/api-token", name="api_token.index", response_model=ApiTokensResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:list"),
):
    pg, items = api_token_repo.sort(sort_qs).paginate(pagination).data()
    return ApiTokensResponse(pagination=pg, api_tokens=items)


@router.post("/api-token", name="api_token.store", response_model=ApiTokenResponse)
async def store(
    form: ApiTokenCreateForm,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:create"),
    user: User = Depends(current_user),
):
    scopes = []
    for requested_scope in form.scopes.split(" "):
        request_scope_satisfied = False
        for user_token in token.scopes:
            # TODO: double check this, pretty lenient
            # if a:b in a:b:c
            if user_token in requested_scope:
                request_scope_satisfied = True
        if not request_scope_satisfied:
            logger.warning(f"Attempt to create unauthorized scope {requested_scope}")
            raise HTTPException(403, detail="unauthorized")
        else:
            scopes.append(requested_scope)

    # TODO: use better randomness

    token = create_bearer_token(
        data={
            "sub": user.id,
            "scopes": " ".join(scopes),
            "dns_server_name": form.dns_server_name,
        }
    )

    data = {
        "scopes": " ".join(scopes),
        "token": str(token.decode()),
        "expires_at": form.expires_at,
        "dns_server_name": form.dns_server_name,
    }

    api_token = api_token_repo.create(data).data()
    return ApiTokenResponse(api_token=api_token)


@router.get(
    "/api-token/{api_token_id}", name="api_token.show", response_model=ApiTokenResponse
)
async def index(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:read"),
):
    if not api_token_repo.exists(api_token_id):
        raise HTTPException(404, detail="Not found")
    api_token = api_token_repo.data()
    return ApiTokenResponse(api_token=api_token)


@router.get(
    "/api-token/{api_token_id}/sensitive",
    name="api_token.show.sensitive",
    response_model=SensitiveApiTokenResponse,
)
async def index(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:read"),
):
    # TODO: require stronger scope
    if not api_token_repo.exists(api_token_id):
        raise HTTPException(404, detail="Not found")
    api_token = api_token_repo.set_data_model(SensitiveApiTokenData).data()
    return SensitiveApiTokenResponse(api_token=api_token)


@router.delete("/api-token/{api_token_id}", response_model=BaseResponse)
async def destroy(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:destroy"),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not api_token_repo.exists(api_token_id):
        return BaseResponse(messages=messages)
    api_token_repo.deactivate(api_token_id)
    return BaseResponse(messages=messages)
