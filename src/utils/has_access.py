from ..db import FoundUser, FoundPost
from typing import Optional
from .exists import exists, post_exists
from .._typing import AccountType
from .perms import check_perms
from strawberry.types import Info
from .exception import exception

__all__ = (
    'has_access',
)

def has_access(
    info: Info,
    user: FoundUser,
    target: Optional[str] = None,
    needed: AccountType = 'admin'
) -> FoundUser:
    """Check if supplied credentials can view the target account."""
    target_model: FoundUser = exists(info, target or user.username)

    if user.username != target_model.username:
        if user.account_type == "user":
            exception(info, 'Insufficent permissions.', 403)
        check_perms(
            info,
            user.account_type,
            target_model.account_type if target else needed
        )

    return target_model