from strawberry.types import Info
from typing import NoReturn, Optional

__all__ = ("exception",)

def exception(
    info: Info,
    message: str,
    status_code: int = 400,
    from_exc: Optional[Exception] = None
) -> NoReturn:
    """Raise an error inside a GraphQL resolver."""
    info.context.response.status_code = status_code
    raise Exception(message) from from_exc