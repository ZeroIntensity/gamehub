import strawberry
import re
from typing_extensions import Annotated
from ..db import UserModel
from ..utils import validate, hash, check_perms, ORDER, check_creds

@strawberry.input(description = "User authentication data.")
class User:
    name: str = strawberry.field(description = 'Name of the user.')
    password: str = strawberry.field(description = 'Password of the user.')

AccountCredentials = Annotated[User, strawberry.argument("Account credentials.")]
 
@strawberry.field(description = "Create a new account.")
def create_account(
    user: Annotated[
        User, 
        strawberry.argument("Data to create the account from.")
    ]
) -> str:
    model = UserModel(username = user.name)
    pattern = r'.*(<|>|\(|\)|\*|&|@|\'|\"|,|\{|\}|\[|\]).*'

    validate({
        model.exists(): f'Name "{user.name}" is already taken.',
        len(user.name) < 4: "Username must be at least 4 characters.",
        len(user.name) > 20: "Username cannot exceed 20 characters.",
        re.match(pattern, user.name): "Invalid username.",
        len(user.password) < 6: "Password must be at least 6 characters."
    })

    model.password = hash(user.password)
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
    
    try:
        target = UserModel(username = username).find()
    except ValueError as e:
        raise Exception(f'User "{username}" was not found.') from e

    model = UserModel(username = credentials.name).find()
    typ = target.account_type
    
    index = ORDER.index(typ) + 1

    if len(ORDER) == index:
        raise Exception(f'"{username}" already has the maximum permissions.')

    next = ORDER[index]
    check_perms(model.account_type, next)
    
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

    try:
        target = UserModel(username = username).find()
    except ValueError as e:
        raise Exception(f'User "{username}" was not found.') from e

    model = UserModel(username = credentials.name).find()
    typ = target.account_type

    index = ORDER.index(typ) - 1

    if index < 0:
        raise Exception(f'"{username}" already has the minimum permissions.')

    pre = ORDER[index]
    check_perms(model.account_type, target.account_type)

    ext = UserModel(username = username).find()
    ext.account_type = pre

    target.update(ext)
    return f'Demoted "{username}" to "{pre}"'
