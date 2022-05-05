from ..db import users
from typing import Optional

__all__ = ('find_username',)

def find_username(name: str) -> Optional[str]:
    """Correctly capitalize the given username."""

    resp: str = ''

    for user in users.find():
        if user['username'].lower() == name.lower():
            resp = user['username']
            return resp

    return None