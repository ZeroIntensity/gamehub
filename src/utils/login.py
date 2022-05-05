from ..db import FoundUser, users, UserModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional

__all__ = ('check_creds',)

def check_creds(username: str, password: str) -> Optional[FoundUser]:
    """Check a users credentials."""
    hasher = PasswordHasher()
    
    try:
        found = False
        for user in users.find():
            if user['username'].lower() == username.lower():
                name = user['username']
                found = True
                
        if not found:
            raise ValueError
            
        # TODO: optimize
        
        model = UserModel(username = name).find()
        hasher.verify(model.password, password)
    except (ValueError, VerifyMismatchError):
        return None

    return model

