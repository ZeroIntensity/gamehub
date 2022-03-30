import strawberry
import re
from typing_extensions import Annotated
from ..db import UserModel
from ..utils import (
    validate, 
    hash, 
    check_perms, 
    ORDER, 
    check_creds,
    exists,
    has_access,
    not_null
)
from typing import Optional
from .._typing import AccountType

@strawberry.input(description = "User authentication data.")
class UserInput:
    name: str = strawberry.field(description = 'Account username.')
    password: str = strawberry.field(description = 'Account password.')

AccountCredentials = Annotated[UserInput, strawberry.argument("Account credentials.")]
TargetAccount = Annotated[
    Optional[str],
    strawberry.argument("Target account to perform operation on. Defaults to self when null.")
]

@strawberry.field(description = "Create a new account.")
def create_account(
    credentials: AccountCredentials
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

@strawberry.field(description = "Promote a user.")
def promote(
    credentials: AccountCredentials,
    username: Annotated[
        str,
        strawberry.argument("Account to promote.")
    ]
) -> str:
    check_creds(credentials.name, credentials.password)
    target = exists(username)

    model = UserModel(username = credentials.name).find()
    typ: AccountType = not_null(target.account_type)
    
    index = ORDER.index(typ) + 1

    if len(ORDER) == index:
        raise Exception(f'"{username}" already has the maximum permissions.')

    next = ORDER[index]
    check_perms(not_null(model.account_type), next)
    
    ext = UserModel(username = username).find()
    ext.account_type = next
    
    target.update(ext)
    return f'Promoted "{username}" to "{next}"'

@strawberry.field(description = "Demote a user.")
def demote(
    credentials: AccountCredentials,
    username: Annotated[
        str,
        strawberry.argument("Account to demote.")
    ]
) -> str:
    check_creds(credentials.name, credentials.password)
    target = exists(username)

    model = UserModel(username = credentials.name).find()
    typ: AccountType = not_null(target.account_type)

    index = ORDER.index(typ) - 1

    if index < 0:
        raise Exception(f'"{username}" already has the minimum permissions.')

    pre = ORDER[index]
    check_perms(not_null(model.account_type), typ)

    ext = UserModel(username = username).find()
    ext.account_type = pre

    target.update(ext)
    return f'Demoted "{username}" to "{pre}"'

@strawberry.field(description = "Delete or terminate an account.")
def delete_account(credentials: AccountCredentials, target: TargetAccount) -> str:
    model = has_access(
        credentials.name, 
        credentials.password, 
        target
    )
    model.delete()

    return f'Deleted user "{target}".'
