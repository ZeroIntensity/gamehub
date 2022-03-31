from strawberry import BasePermission
from strawberry.types import Info
from fastapi import Request, Depends
from typing import Any
import re
from base64 import urlsafe_b64decode as decode
from strawberry.fastapi import BaseContext
from ..db import FoundUser, UserModel
from binascii import Error

class Context(BaseContext):
    def __init__(self, user: FoundUser) -> None:
        self.user = user

async def get_context(ctx = Depends(ctx_dependency)):
    return ctx

class Authenticated(BasePermission):
    message = "Authentication is required."
    
    def has_permission(self, _: Any, info: Info, **kwargs) -> bool:
        request: Request = info.context["request"]
        auth = request.headers.get('Authorization')

        if not auth:
            return False

        if not re.match('Basic .+', auth):
            return False
        
        try:
            decoded: bytes = decode(auth)
        except Error:
            return False
        
        split: list = decoded.decode().split(':', maxsplit = 1)
        
        if len(split) >= 1:
            return False

        username = split[0]
        password = split[1]

        return True


