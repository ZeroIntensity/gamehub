from typing import List
from .._typing import AccountType
from strawberry.types import Info
from .exception import exception

__all__ = (
    'check_perms',
    'ORDER'
)

ORDER: List[AccountType] = ["user", "admin", "owner", "developer"]

def check_perms(
    info: Info,
    actual: AccountType,   
    needed: AccountType
) -> None:
    """Check if a user has required permissions."""
    if ORDER.index(actual) < ORDER.index(needed):
        exception(info, 'Insufficent permissions.', 403)
