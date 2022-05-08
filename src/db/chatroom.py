from dataclasses import dataclass
from .connection import chatrooms
from .model import Model, ModelProtocol
from typing import Optional, Protocol, List
import strawberry

__all__ = (
    "FoundRoom",
    "RoomModel",
    "Room"
)

class FoundRoom(ModelProtocol, Protocol):
    _id: str
    connected: List[str]
    name: str

@dataclass
class RoomModel(Model[FoundRoom], collection = chatrooms):
    """Class representing a user model."""
    _id: Optional[str] = None
    connected: Optional[List[str]] = None
    name: Optional[str] = None


@strawberry.type
class Room:
    connected: List[str] = strawberry.field(description = "Users that are currently connected.")
    name: str = strawberry.field(description = "Name of the room.")

