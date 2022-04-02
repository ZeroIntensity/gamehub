# sourcery skip: avoid-builtin-shadow
from .model import Model, ModelProtocol
import strawberry
from typing import Optional, Protocol
from dataclasses import dataclass
from .connection import posts

__all__ = (
    'FoundPost',
    'PostModel',
    'Post'
)

class FoundPost(ModelProtocol, Protocol):
    _id: str
    author: str
    content: str
    epoch: float
    id: str

@dataclass
class PostModel(Model[FoundPost], collection = posts):
    _id: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
    epoch: Optional[float] = None
    id: Optional[str] = None

@strawberry.type(description = "Post object.")
class Post:
    author: str = strawberry.field(description = "Author of the post.")
    content: str = strawberry.field(description = "Content of the post.")
    epoch: float = strawberry.field(description = "UNIX epoch creation date of the post.")
    id: str = strawberry.field(description = "ID of the post.")