from fastapi import APIRouter, WebSocket, Depends, Request
from ..gql import ctx_dependency
from ..utils.template import template
from typing import List

prefix: str = '/chatrooms'
router = APIRouter()

class Room:
    def __init__(self):
        self._connected: List[str] = []

    @property
    def connected(self) -> List[str]:
        """List of users connected to the room."""
        return self._connected

ROOMS: List[Room] = []



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@router.get('/')
async def chatrooms(request: Request, ctx = Depends(ctx_dependency)):
    return template(
        'chatrooms.html',
        request,
        ctx
    )