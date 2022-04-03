import strawberry
import re
from typing_extensions import Annotated
from ..db import UserModel, FoundUser
from ..utils import (
    validate, 
    hash, 
    check_perms, 
    ORDER, 
    exists,
    has_access,
    not_null
)
from typing import Optional
from .._typing import AccountType
from .permissions import Authenticated, HasAdmin
from strawberry.types import Info

__all__ = (
    "create_account",
    "delete_account",
    "promote",
    "demote",
    "TargetAccount"
)

@strawberry.input(description = "User authentication data.")
class UserInput:
    name: str = strawberry.field(description = 'Account username.')
    password: str = strawberry.field(description = 'Account password.')

TargetAccount = Annotated[
    Optional[str],
    strawberry.argument("Target account to perform operation on. Defaults to self when null.")
]

@strawberry.field(description = "Create a new account.")
def create_account(
    credentials: Annotated[
        UserInput,
        strawberry.argument("Credentials to account from.")
    ]
) -> str:
    model = UserModel(username = credentials.name)
    pattern = r'.*(<|>|\(|\)|\*|&|@|\'|\"|,|\{|\}|\[|\]).*'

    validate({
        model.exists(): f'Name "{credentials.name}" is already taken.',
        len(credentials.name) < 4: "Username must be at least 4 characters.",
        len(credentials.name) > 20: "Username cannot exceed 20 characters.",
        bool(re.match(pattern, credentials.name)): "Invalid username.",
        len(credentials.password) < 6: "Password must be at least 6 characters."
    })

    model.password = hash(credentials.password)
    model.account_type = "user"
    
    model.save()

    return "Successfully created account."

@strawberry.field(
    description = "Promote a user.",
    permission_classes = [Authenticated, HasAdmin]
)
def promote(
    info: Info,
    username: Annotated[
        str,
        strawberry.argument("Account to promote.")
    ]
) -> str:
    model: FoundUser = info.context.user
    target = exists(username)

    typ: AccountType = not_null(target.account_type)
    
    index = ORDER.index(typ) + 1

    if len(ORDER) == index:
        raise Exception(f'"{username}" already has the maximum permissions.')

    next_item = ORDER[index]
    check_perms(model.account_type, next_item)
    
    ext = UserModel(username = username).find()
    ext.account_type = next_item
    
    target.update(ext)
    return f'Promoted "{username}" to "{next_item}"'

@strawberry.field(
    description = "Demote a user.",
    permission_classes = [Authenticated]
)
def demote(
    info: Info,
    username: Annotated[
        str,
        strawberry.argument("Account to demote.")
    ]
) -> str:
    model: FoundUser = info.context.user
    target = exists(username)

    typ: AccountType = target.account_type

    index = ORDER.index(typ) - 1

    if index < 0:
        raise Exception(f'"{username}" already has the minimum permissions.')

    pre = ORDER[index]
    check_perms(model.account_type, typ)

    ext = UserModel(username = username).find()
    ext.account_type = pre

    target.update(ext)
    return f'Demoted "{username}" to "{pre}"'

@strawberry.field(
    description = "Delete or terminate an account.",
    permission_classes = [Authenticated]
)
def delete_account(info: Info, target: TargetAccount = None) -> str:
    user: FoundUser = info.context.user
    model = has_access(user, target)
    model.delete()

    return f'Deleted user "{target or user.username}".'
