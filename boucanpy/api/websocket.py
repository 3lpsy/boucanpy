import json
from urllib.parse import urlparse, parse_qs
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi import HTTPException
import aioredis

from boucanpy.core import logger
from boucanpy.core.security import (
    verify_jwt_token,
    token_has_required_scopes,
    current_user,
)
from boucanpy.core import TokenPayload
from boucanpy.core.user import UserRepo

from boucanpy.db import session
from boucanpy.broadcast import make_redis, make_broadcast_url, make_subscriber

# TODO: clean up this mess


async def broadcast_index(websocket: WebSocket):
    try:
        logger.info("broadcast_index@websocket.py - Accepting websockets")
        await websocket.accept()
    except Exception as e:
        logger.critical(f"broadcast_index@websocket.py - Accept: Error: {str(type(e))}")
        logger.critical(f"broadcast_index@websocket.py - Accept: Trace: {str(e)}")
        logger.critical(
            f"broadcast_index@websocket.py - Accept:Not closing or unsubscribing"
        )
        return 1

    try:
        while True:
            logger.info("broadcast_index@websocket.py - Receiving json")
            data = await websocket.receive_json()
            logger.info("broadcast_index@websocket.py - Received json: " + str(data))
            logger.info(
                "broadcast_index@websocket.py - Sending message: "
                + str({"message": "greetings"})
            )
            await websocket.send_json({"message": "greetings"})
    except Exception as e:
        logger.critical(
            f"broadcast_index@websocket.py - Receieve/Send: Error: {str(type(e))}"
        )
        logger.critical(
            f"broadcast_index@websocket.py - Receieve/Send: Trace: {str(e)}"
        )
        logger.critical(
            f"broadcast_index@websocket.py - Receieve/Send: Not closing or unsubscribing"
        )
        return 1

    await websocket.close()


# TODO: clean up this mess
async def broadcast_auth(websocket: WebSocket):
    try:
        await websocket.accept()
    except Exception as e:
        logger.critical(f"broadcast_auth@websocket.py - Accept Error: {str(type(e))}")
        logger.critical(f"broadcast_auth@websocket.py - Accept Trace: {str(e)}")
        return 1

    params = parse_qs(urlparse(str(websocket.url)).query)
    token = verify_jwt_token(params["ws_access_token"][0])
    if not token_has_required_scopes(token, []):  # TODO: check scopes later
        raise HTTPException(403, detail="Forbidden")
    user_repo = UserRepo(session())
    user = await current_user(token, user_repo)

    subscriber, channel = await make_subscriber("auth")

    try:
        while await channel.wait_message():
            logger.info("broadcast_auth@websocket.py - Waiting for message")
            msg = await channel.get(encoding="utf-8")
            logger.info("broadcast_auth@websocket.py - Received message: " + str(msg))
            data = json.loads(msg)
            logger.info("broadcast_auth@websocket.py - Sending message: " + str(data))
            await websocket.send_json(data)
    except Exception as e:
        logger.critical(
            f"broadcast_auth@websocket.py - Receieve/Send: Error: {str(type(e))}"
        )
        logger.critical(f"broadcast_auth@websocket.py - Receieve/Send: Trace:{str(e)}")
        logger.critical(
            f"broadcast_auth@websocket.py - Receieve/Send: Not closing or unsubscribing"
        )

        return 1

    logger.info(f"broadcast_index@websocket.py - Attempting to unsuscribe")
    await subscriber.unsubscribe("channel:auth")
    logger.info(f"broadcast_index@websocket.py: Websocket - Attempting to close socket")
    await websocket.close()

