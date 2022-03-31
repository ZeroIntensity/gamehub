from strawberry import BasePermission
from strawberry.types import Info
from typing import Any, Optional, Protocol

class Authenticated(BasePermission):
    message = "Authentication is required."

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        pass
