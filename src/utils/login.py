from ..db import UserModel, FoundUser
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional

__all__ = ('check_creds',)

def check_creds(username: str, password: str) -> Optional[FoundUser]:
    """Check a users credentials."""

    tmp = UserModel(username = username)
    hasher = PasswordHasher()
    
    try:
        model = tmp.find()
        hasher.verify(model.password, password)
    except (ValueError, VerifyMismatchError) as e:
        return None

    return model

