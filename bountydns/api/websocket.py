import json
from urllib.parse import urlparse, parse_qs
from starlette.websockets import WebSocket
from fastapi import HTTPException
import aioredis

from bountydns.core import logger
from bountydns.core.security import (
    verify_jwt_token,
    token_has_required_scopes,
    current_user,
)
from bountydns.core.entities import TokenPayload, UserRepo
from bountydns.db import session
from bountydns.broadcast import make_redis, make_broadcast_url, make_subscriber


async def broadcast_index(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({"message": "greetings"})
    await websocket.close()


# TODO: clean up this mess
async def broadcast_authed_index(websocket: WebSocket):
    await websocket.accept()
    params = parse_qs(urlparse(str(websocket.url)).query)
    token = verify_jwt_token(params["ws_access_token"][0])
    if not token_has_required_scopes(token, []):  # TODO: check scopes later
        raise HTTPException(403, detail="Forbidden")
    user_repo = UserRepo(session())
    user = current_user(token, user_repo)

    subscriber, channel = await make_subscriber("auth")

    while await channel.wait_message():
        msg = await channel.get(encoding="utf-8")
        data = json.loads(msg)
        await websocket.send_json(data)

    await subscriber.unsubscribe("channel:auth")
    await websocket.close()
