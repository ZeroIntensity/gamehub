from fastapi import security
from strawberry import BasePermission
from strawberry.types import Info
from fastapi import Depends
from typing import Any, Optional
from strawberry.fastapi import BaseContext
from ..db import FoundUser
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..utils import check_creds, check_perms

__all__ = (
    'Authenticated',
    'HasAdmin'
)

security = HTTPBasic(auto_error = False)

class Context(BaseContext):
    def __init__(self, user: Optional[FoundUser]) -> None:
        self.user = user

def ctx_dependency(credentials: HTTPBasicCredentials = Depends(security)) -> Context:
    user = check_creds(credentials.username, credentials.password) \
            if credentials else None
    return Context(user = user)

async def get_context(ctx = Depends(ctx_dependency)):
    return ctx

class Authenticated(BasePermission):
    message = "Invalid username or password."
    
    def has_permission(self, _: Any, info: Info, **kwargs) -> bool:
        return bool(info.context.user)

class HasAdmin(BasePermission):
    message = "Insufficent permissions."

    def has_permission(self, _: Any, info: Info, **kwargs):
        try:
            check_perms(info.context.user.account_type, 'admin')
            return True
        except: # function raises Exception, which is default by bare except clause
            return False