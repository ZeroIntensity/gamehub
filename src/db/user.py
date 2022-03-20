from .model import Model
from .connection import db
from .._typing import Argon2Hash
from typing import TypedDict, Optional

__all__ = (
    'User',
    'UserDictionary'
)

class UserDictionary(TypedDict):
    username: str
    password: Argon2Hash

class User(Model):
    """Class representing a user."""
    def __init__(self, username: str, password: Argon2Hash, _id: Optional[str] = None):
        self._username = username
        self._password = password
        self._is_real = False
        self._id = _id

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> Argon2Hash:
        return self._password

    @property
    def is_real(self) -> bool:
        return self._is_real

    @property
    def document_id(self) -> Optional[str]:
        return self._id

    @is_real.setter
    def is_real(self, value: bool) -> None:
        self._is_real = value

    def create(self) -> str:
        self.is_real = True
        return db["users"].insert_one(self.as_dict()).inserted_id

    def as_dict(self) -> UserDictionary:
        return {
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def find(cls, values: dict):
        document = db["users"].find_one(values)
        
        if document:
            return cls(**document)

    