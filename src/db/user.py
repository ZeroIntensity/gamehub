from dataclasses import dataclass
from .._typing import Argon2Hash
from .connection import users
from .model import Model
from typing import Optional

@dataclass
class UserModel(Model, collection = users):
    """Class representing a user model."""
    username: Optional[str] = None
    password: Optional[Argon2Hash] = None
