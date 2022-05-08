from fastapi import (
    APIRouter,
    Request,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    Cookie,
    status
)
from ..gql import ctx_dependency, get_rooms
from ..utils.template import template
from ..utils import decode_jwt
from typing import Optional, List, Dict
from ..db import RoomModel, chatrooms
from .._typing import RoomMessage
import bleach

router = APIRouter()
prefix: str = '/chatrooms'

@router.get('/')
def index(request: Request, ctx = Depends(ctx_dependency)):
    return template(
        'chatrooms.html',
        request,
        ctx,
        rooms = get_rooms(),
        len = len
    )

class RoomManager:
    def __init__(self, name: str) -> None:
        self.active_connections: List[WebSocket] = []
        self.room_name = name

    async def connect(self, websocket: WebSocket, username: str) -> bool:
        await websocket.accept()
        model = RoomModel(name = self.room_name).find()

        if username in model.connected:
            await websocket.close(code = status.WS_1008_POLICY_VIOLATION)
            return False

        model.connected.append(username)
        model.update()

        self.active_connections.append(websocket)
        await self.sys_message(f"{username} has joined the room.")
        return True

    async def disconnect(self, websocket: WebSocket, username: str) -> None:
        model = RoomModel(name = self.room_name).find()
        model.connected.remove(username)
        model.update()

        self.active_connections.remove(websocket)
        await self.sys_message(f"{username} has left the room.")

    async def _broadcast(self, json: RoomMessage) -> None:
        for connection in self.active_connections:
            await connection.send_json(json)

    async def send_message(self, message: str, author: str) -> None:
        await self._broadcast(
            {
                "type": "message",
                "message": message,
                "author": author
            }
        )

    async def sys_message(self, message: str) -> None:
        await self._broadcast(self.make_sys_message(message))

    def make_sys_message(self, message: str) -> RoomMessage:
        return {
            "type": "notification",
            "message": message,
            "author": "sys"
        }
        
    

MANAGERS: Dict[str, RoomManager] = {}

for room in chatrooms.find():
    model = RoomModel(name = room['name']).find()
    model.connected = []
    model.update()

async def handle_auth(
    websocket: WebSocket,
    auth: Optional[str] = Cookie(None),
):  
    if not auth:
        return await websocket.close(code = status.WS_1008_POLICY_VIOLATION)

    decoded = decode_jwt(auth)

    if not decoded:
        return await websocket.close(code = status.WS_1008_POLICY_VIOLATION)

    return decoded["user_id"]

@router.websocket('/{name}/connect')
async def connect(
    websocket: WebSocket,
    name: str,
    username: Optional[str] = Depends(handle_auth)
):
    if not username:
        return

    name = name.replace('-', '#')

    if name not in MANAGERS:
        MANAGERS[name] = RoomManager(name)

    manager = MANAGERS[name]
    success: bool = await manager.connect(websocket, username)

    if not success:
        return

    try:
        while True:
            data = await websocket.receive_text()

            if 300 < len(data):
                await websocket.send_json(
                    manager.make_sys_message(
                        "Message cannot exceed 300 characters."
                    )
                )

            elif not data:
                await websocket.send_json(
                    manager.make_sys_message(
                        "Message is required."
                    )
                )

            else:
                await manager.send_message(bleach.clean(data), username)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, username)

