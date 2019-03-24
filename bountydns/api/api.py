from pathlib import Path
from dotenv import load_dotenv
from bountydns.core.utils import root_dir
from fastapi import FastAPI, APIRouter

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from bountydns.core import logger
from bountydns.api.routers import routers
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url

db_register("api", make_db_url("api"))

from bountydns.api import config  # environment must be loaded

# CORS
api = FastAPI(title=config.API_PROJECT_NAME, openapi_url="/api/v1/openapi.json")

origins = []

# Set all CORS enabled origins
if config.API_CORS_ORIGINS:
    origins_raw = config.API_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    logger.debug(f"registering cors origins {origins}")
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

main_router = APIRouter()

for r, ropts in routers:
    logger.debug(f"registering router {str(r)} {str(ropts)}")
    main_router.include_router(r, **ropts)

api.include_router(main_router, prefix=config.API_V1_STR)


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = session("api")
    response = await call_next(request)
    request.state.db.close()
    return response
