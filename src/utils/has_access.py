from ..db import FoundUser

from typing import Optional
from .login import check_creds
from .exists import exists
from .._typing import AccountType
from .perms import check_perms

__all__ = ['has_access']

def has_access(
    username: str,
    password: str,
    target: Optional[str] = None,
    needed: AccountType = 'admin'
) -> FoundUser:
    """Check if supplied credentials can view the target account."""
    model = check_creds(username, password)
    target_model: FoundUser = exists(target or username)

    if model.username != target_model.username:
        check_perms(model.account_type, needed)

    return target_model
