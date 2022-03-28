from ..db import UserModel
from typing import Union, NoReturn, Optional
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
) -> Union[UserModel, NoReturn]:
    """Check if supplied credentials can view the target account."""
    model = check_creds(username, password)
    target = exists(target or username)

    if model.username != target.username:
        check_perms(model.account_type, needed)

    return target
