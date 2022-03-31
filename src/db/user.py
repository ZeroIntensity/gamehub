from dataclasses import dataclass
from .._typing import Argon2Hash, AccountType
from .connection import users
from .model import Model, ModelProtocol
from typing import Optional, Protocol

__all__ = (
    'UserModel',
    'FoundUser'
)

class FoundUser(ModelProtocol, Protocol):
    _id: str
    username: str
    password: str
    account_type: AccountType


@dataclass
class UserModel(Model[FoundUser], collection = users):
    """Class representing a user model."""
    _id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[Argon2Hash] = None
    account_type: Optional[AccountType] = None
