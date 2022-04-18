from typing import List
from .._typing import AccountType
from strawberry.types import Info
from .exception import exception

__all__ = (
    'check_perms',
    'ORDER',
    'check_perms_bool'
)

ORDER: List[AccountType] = ["user", "admin", "owner", "developer"]

def check_perms_bool(
    actual: AccountType,   
    needed: AccountType
) -> bool:
    """Check if a user has required permissions."""
    return not ORDER.index(actual) < ORDER.index(needed)


def check_perms(
    info: Info,
    actual: AccountType,   
    needed: AccountType
) -> None:
    """Check if a user has required permissions."""
    if not check_perms_bool(actual, needed):
        exception(info, 'Insufficent permissions.', 403)
