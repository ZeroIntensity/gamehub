# sourcery skip: avoid-builtin-shadow
from .model import Model, ModelProtocol
from typing import Optional, Protocol, List
from dataclasses import dataclass
from .._typing import Comment as CommentType, PostID
from .connection import games
import strawberry

__all__ = (
    "FoundGame",
    "GameModel",
    "Comment",
    "Game",
    "GameInput"
)

@strawberry.type(description = "Comment object.")
class Comment:
    author: str = strawberry.field(description = "Author of the comment")
    likes: List[str] = strawberry.field(description = "Array containing users who have liked the comment.")
    content: str = strawberry.field(description = "Content of the comment.")
    epoch: float = strawberry.field(description = "UNIX epoch creation date of the comment.")
    id: str = strawberry.field(description = "ID of the comment.")

class FoundGame(ModelProtocol, Protocol):
    _id: str
    name: str
    likes: List[str]
    comments: List[CommentType]
    data: str

@dataclass
class GameModel(Model[FoundGame], collection = games):
    _id: Optional[str] = None
    name: Optional[str] = None
    likes: Optional[List[str]] = None
    comments: Optional[List[CommentType]] = None
    data: Optional[str] = None

@strawberry.type(description = "Game object.")
class Game:
    name: str = strawberry.field(description = "Name of the game.")
    likes: List[str] = strawberry.field(description = "Array containing users who have liked the game.")
    comments: List[Comment] = strawberry.field(description = "Array of comments.")
    data: str = strawberry.field(description = "Where the game is stored.")

@strawberry.input(description = "Game creation data.")
class GameInput:
    name: str = strawberry.field(description = "Name of the game.")
    data: str = strawberry.field(description = "Game data location.")
