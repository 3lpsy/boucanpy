from fastapi import APIRouter
import aioredis
from bountydns.broadcast import make_redis, make_broadcast_url

router = APIRouter()
options = {"prefix": ""}


@router.get("/util/ws-test", name="util.ws-test")
async def ws_test():
    publisher = await aioredis.create_redis(make_broadcast_url())
    res = await publisher.publish_json(
        "channel:auth", {"type": "MESSAGE", "name": "TESTING_WS", "payload": ""}
    )
    return {"status": "up"}
