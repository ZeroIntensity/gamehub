from dataclasses import dataclass
from .._typing import Argon2Hash, AccountType, ProfileComment as ProfileCommentType
from .connection import users
from .model import Model, ModelProtocol
from typing import Optional, Protocol, List
import strawberry

__all__ = (
    'UserModel',
    'FoundUser',
    'ProfileComment',
    'User'
)

@strawberry.type(description = "Object representing a profile comment.")
class ProfileComment:
    game: str = strawberry.field(description = "Name of the game.")
    epoch: float = strawberry.field(
        description = "UNIX epoch creation date of the comment."
    )
    content: str = strawberry.field(description = "Content of the comment.")


class FoundUser(ModelProtocol, Protocol):
    _id: str
    username: str
    password: str
    account_type: AccountType
    likes: List[str]
    comments: List[ProfileCommentType]

@dataclass
class UserModel(Model[FoundUser], collection = users):
    """Class representing a user model."""
    _id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[Argon2Hash] = None
    account_type: Optional[AccountType] = None
    likes: Optional[List[str]] = None
    comments: Optional[List[ProfileCommentType]] = None

@strawberry.type
class User:
    username: str = strawberry.field(
        description = "Account username.",
        name = "name"
    )
    account_type: str = strawberry.field(description = "Account permissions.")
    likes: List[str] = strawberry.field(
        description = "Array of games that the user has liked."
    )
    comments: List[ProfileComment] = strawberry.field(
        description = "Array of comments that the user has posted on various games."
    )

