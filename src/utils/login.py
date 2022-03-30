from ..db import UserModel
from typing import Union, NoReturn
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def check_creds(username: str, password: str) -> Union[UserModel, NoReturn]:
    """Check a users credentials."""

    tmp = UserModel(username = username)
    hasher = PasswordHasher()
    
    try:
        model = tmp.find()
        
        assert model.password 
        hasher.verify(model.password, password)
    except (ValueError, VerifyMismatchError) as e:
        raise Exception("Invalid username or password.") from e

    return model

