from fastapi import APIRouter

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-response", name="dns_response.index")
async def index():
    return "logging in"


@router.get("/dns-response/{dns_response_id}", name="dns_response.show")
async def show(dns_response_id: int):
    return "logging in"


@router.post("/dns-response", name="dns_response.store")
async def store():
    return "logging in"


@router.put("/dns-response/{dns_response_id}", name="dns_response.update")
async def update(dns_response_id: int):
    return "logging in"


@router.delete("/dns-response/{dns_response_id}", name="dns_response.destroy")
async def destroy(dns_response_id: int):
    return "logging in"
