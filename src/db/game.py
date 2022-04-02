from .model import Model, ModelProtocol
from typing import Optional, Protocol, List
from dataclasses import dataclass
from .._typing import Comment as CommentType
from .connection import games
import strawberry

__all__ = (
    "FoundGame",
    "GameModel",
    "Comment",
    "Game",
    "GameInput"
)

@strawberry.type
class Comment:
    author: str = strawberry.field(description = "Author of the comment")
    likes: int = strawberry.field(description = "Amount of likes the comment currently has.")
    content: str = strawberry.field(description = "Content of the comment.")

class FoundGame(ModelProtocol, Protocol):
    _id: str
    name: str
    likes: int
    comments: List[CommentType]
    data: str

@dataclass
class GameModel(Model[FoundGame], collection = games):
    _id: Optional[str] = None
    name: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[List[CommentType]] = None
    data: Optional[str] = None

@strawberry.type(description = "Game object.")
class Game:
    name: str = strawberry.field(description = "Name of the game.")
    likes: int = strawberry.field(description = "Amount of likes the game currently has.")
    comments: List[Comment] = strawberry.field(description = "Array of comments.")
    data: str = strawberry.field(description = "Where the game is stored.")

@strawberry.input(description = "Game creation data.")
class GameInput:
    name: str
    data: str
