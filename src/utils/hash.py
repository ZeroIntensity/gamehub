from argon2 import PasswordHasher
from .._typing import Argon2Hash

__all__ = ('hash',)

hasher = PasswordHasher()

def hash(raw: str) -> Argon2Hash:
    """Hash a string using Argon2."""
    return Argon2Hash(hasher.hash(raw))
