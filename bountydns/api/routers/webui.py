from fastapi import APIRouter, Depends, File
from starlette.responses import HTMLResponse
from bountydns.core.utils import web_dir
from bountydns.api.jinja2 import jinja2

router = APIRouter()
options = {"prefix": ""}


@router.get("/webui", name="webui.index")
async def webui_index():
    # TODO: confirm this isn't vuln to path/dir traversal
    template = jinja2.get_template("index.html")
    content = template.render()
    return HTMLResponse(content=content, status_code=200)


@router.get("/webui/{file_name}", name="webui.show")
async def webui_show(file_name: str):
    # TODO: confirm this isn't vuln to path/dir traversal
    template = jinja2.get_template(file_name)
    content = template.render()

    return HTMLResponse(content=content, status_code=200)
