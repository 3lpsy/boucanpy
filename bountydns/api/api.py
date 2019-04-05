from pathlib import Path
from os.path import join
from urllib.parse import urlparse
from dotenv import load_dotenv
from bountydns.core.utils import root_dir
from fastapi import FastAPI, APIRouter

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.routing import Router, Mount
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, FileResponse, JSONResponse
from starlette.exceptions import HTTPException

from bountydns.core.utils import webui_dir, landing_dir
from bountydns.core import logger
from bountydns.api.routers import routers
from bountydns.api.websocket import broadcast_index, broadcast_authed_index
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url

db_register(make_db_url())

from bountydns.api import (
    config,
)  # environment must be loaded, dabatabse must be registerd


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

from starlette.websockets import WebSocket

# public broadcast
api.add_websocket_route("/broadcast", broadcast_index, name="broadcast.index")
api.add_websocket_route(
    "/broadcast/auth", broadcast_authed_index, name="broadcast.authed.index"
)


@api.get("/")
async def webui_redir():
    return RedirectResponse(url="/landing/", status_code=302)


# served by nginx
if Path(landing_dir("index.html")).is_file():

    @api.get("/landing/")
    async def web_index():
        return FileResponse(landing_dir("index.html"))

    api.mount("/landing", StaticFiles(directory=landing_dir()))

# served by nginx
if Path(webui_dir("dist")).is_dir():

    # served by nginx
    @api.get("/webui")
    async def webui_redir():
        return RedirectResponse(url="/webui/", status_code=302)

    # served by nginx w/ slight rewrite
    @api.get("/webui/assets")
    async def webui_index():
        return FileResponse(webui_dir(join("dist", "index.html")))

    api.mount("/webui/assets", StaticFiles(directory=webui_dir("dist")))

# TODO: make core handler
@api.exception_handler(404)
async def http_exception(request, exc):
    url = urlparse(str(request.url))
    if not url.path.startswith("/api/v1"):
        if (
            Path(webui_dir("dist")).is_dir()
            and Path(webui_dir(join("dist", "index.html"))).is_file()
        ):
            return FileResponse(webui_dir(join("dist", "index.html")))
    return JSONResponse({"detail": "Not Found"}, status_code=404)


@api.exception_handler(500)
async def http_exception(request, exc):
    return JSONResponse({"detail": "Server Error"}, status_code=500)


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = session()
    response = await call_next(request)
    request.state.db.close()
    return response
