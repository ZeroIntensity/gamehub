import strawberry
from .permissions import Authenticated, HasAdmin
from strawberry.types import Info
from typing_extensions import Annotated
from ..db import RoomModel
from ..utils import exception

__all__ = (
    "create_room",
    "delete_room"
)

RoomName = Annotated[str, strawberry.argument("Name of the room")]

@strawberry.field(
    description = "Create a new chat room.",
    permission_classes = [Authenticated, HasAdmin]
)
def create_room(
    info: Info,
    name: RoomName
) -> str:
    model = RoomModel(name = name)

    if model.exists():
        exception(info, f'Room with the name "{name}" already exists.')
    
    model.connected = []
    model.save()

    return "Successfully created room."

@strawberry.field(
    description = "Delete a chat room.",
    permission_classes = [Authenticated, HasAdmin]
)
def delete_room(info: Info, name: RoomName) -> str:
    model = RoomModel(name = name)

    if not model.exists():
        exception(info, f'Room with the name "{name}" does not exist.')

    model.delete()
    return "Successfully deleted room."