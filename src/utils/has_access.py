from ..db import FoundUser

from typing import Optional
from .login import check_creds
from .exists import exists
from .._typing import AccountType
from .perms import check_perms

__all__ = ['has_access']

def has_access(
    user: FoundUser,
    target: Optional[str] = None,
    needed: AccountType = 'admin'
) -> FoundUser:
    """Check if supplied credentials can view the target account."""
    target_model: FoundUser = exists(target or user.username)

    if user.username != target_model.username:
        check_perms(user.account_type, target_model.account_type if target else needed)

    return target_model
