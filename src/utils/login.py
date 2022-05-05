from ..db import FoundUser, UserModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
from .find_username import find_username

__all__ = ('check_creds',)

def check_creds(username: str, password: str) -> Optional[FoundUser]:
    """Check a users credentials."""
    hasher = PasswordHasher()
    
    try:
        name = find_username(username)
        
        if not name:
            raise ValueError
        
        model = UserModel(username = name).find()
        hasher.verify(model.password, password)
    except (ValueError, VerifyMismatchError):
        return None

    return model

