from typing import List, Union, NoReturn
from .._typing import AccountType

__all__ = (
    'check_perms',
    'ORDER'
)

ORDER: List[AccountType] = ["user", "admin", "owner", "developer"]

def check_perms(
    actual: AccountType,   
    needed: AccountType
) -> Union[None, NoReturn]:
    """Check if a user has required permissions."""
    if ORDER.index(actual) < ORDER.index(needed):
        raise Exception('Insufficent permissions.')
