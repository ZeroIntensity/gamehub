from .model import Model, ModelProtocol
from typing import Optional, Protocol, List
from dataclasses import dataclass
from .._typing import Comment
from .connection import games

__all__ = (
    "FoundGame",
    "GameModel"
)

class FoundGame(ModelProtocol, Protocol):
    _id: str
    name: str
    likes: int
    comments: List[Comment]


@dataclass
class GameModel(Model[FoundGame], collection = games):
    _id: Optional[str] = None
    name: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[List[Comment]] = None

