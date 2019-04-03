from starlette.websockets import WebSocket


async def broadcast_index(websocket: WebSocket):
    print(websocket)
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({"message": "greetings"})
    await websocket.close()


async def broadcast_authed_index(ws_auth_token: str, websocket: WebSocket):
    print(ws_auth_token)
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({"message": "greetings"})
    await websocket.close()
