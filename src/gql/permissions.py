from fastapi import security, Request, HTTPException
from strawberry import BasePermission
from strawberry.types import Info
from fastapi import Depends
from typing import Any, Optional
from strawberry.fastapi import BaseContext
from ..db import FoundUser, UserModel, Termination, users
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils import check_perms, decode_jwt, not_null

__all__ = (
    'Authenticated',
    'HasAdmin',
    'ctx_dependency',
    'get_context',
    'Context'
)

class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error = False)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = \
            await super(JWTBearer, self).__call__(request)

        if not credentials:
            token: Optional[str] = request.cookies.get('auth')

            if not token:
                return None

            credentials = HTTPAuthorizationCredentials(
                scheme = "Bearer",
                credentials = token
            )
        
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code = 403, detail = "Invalid authentication scheme.")
        
        decoded = decode_jwt(credentials.credentials)

        if not decoded:
            raise HTTPException(status_code = 403, detail = "Invalid or expired token.")
        
        termination = Termination(username = decoded['user_id'].lower())

        if termination.exists():
            raise HTTPException(status_code = 410, detail = f"Account has been terminated: {termination.find().reason}")

        return credentials.credentials

security = JWTBearer()

class Context(BaseContext):
    def __init__(self, user: Optional[FoundUser]) -> None:
        self.user = user

def ctx_dependency(
    credentials: Optional[str] = Depends(security)
) -> Context:
    if not credentials:
        return Context(user = None)
    
    payload = not_null(decode_jwt(credentials))
    name = None
    
    for user in users.find():
        if user['username'].lower() == payload["user_id"].lower():
            name = payload['user_id']
    
    try:
        return Context(user = UserModel(username = name).find())
    except ValueError:
        return Context(user = None)

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
            check_perms(info, info.context.user.account_type, 'admin')
            return True
        except Exception:
            return False
