from ..db import UserModel
from typing import Union, NoReturn

__all__ = ['exists']

def exists(username: str) -> Union[UserModel, NoReturn]:
    """Check if a user exists inside a GraphQL resolver."""

    try:
        target = UserModel(username = username).find()
    except ValueError as e:
        raise Exception(f'User "{username}" does not exist.') from e

    return target
