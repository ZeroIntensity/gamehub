from ..db import UserModel, FoundUser
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def check_creds(username: str, password: str) -> FoundUser:
    """Check a users credentials."""

    tmp = UserModel(username = username)
    hasher = PasswordHasher()
    
    try:
        model = tmp.find()
        hasher.verify(model.password, password)
    except (ValueError, VerifyMismatchError) as e:
        raise Exception("Invalid username or password.") from e

    return model

