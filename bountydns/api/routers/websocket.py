from fastapi import APIRouter

from starlette.websockets import WebSocket
from nejma.ext.starlette import WebSocketEndpoint
from nejma.layers import Channel, channel_layer

router = APIRouter()


@router.get("/ws-test")
async def ws_test():
    for k, group in channel_layer.groups.items():
        print(k, group)
        channel_layer.group_send(group, {"hello": "darkness"})


@router.websocket_route("/ws")
class Chat(WebSocketEndpoint):
    encoding = "json"

    async def on_receive(self, websocket, data):
        print("RECEIVED DATA", websocket, data)
        room_id = data["room_id"]

        if message.strip():
            group = f"group_{room_id}"

            self.channel_layer.add(group, self.channel)

            payload = {"room_id": "You Joined" + room_id}
            await self.channel_layer.group_send(group, payload)
