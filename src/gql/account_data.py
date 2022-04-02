import strawberry
from .account import TargetAccount
from ..utils import has_access, exists
from strawberry.types import Info
from typing_extensions import Annotated

__all__ = (
    "user_data",
    "can_access"
)

First = Annotated[
    str,
    strawberry.argument("Account to check permissions for.")
]
Second = Annotated[
    str,
    strawberry.argument("Account to extract needed permissions from.")
]

@strawberry.type
class User:
    username: str = strawberry.field(
        description = "Account username.",
        name = "name"
    )
    account_type: str = strawberry.field(description = "Account permissions.")

@strawberry.field(description = 'Get data of a user.')
def user_data(
    info: Info,
    target: TargetAccount = None
) -> User:
    model_dict = has_access(info.context.user, target) \
        .make_dict()
    
    for i in ['_id', 'password']:
        del model_dict[i]    

    return User(**model_dict)

@strawberry.field(description = "Check whether a user has access to a target.")
def can_access(
    first: First,
    second: Second
) -> bool:
    try:
        has_access(exists(first), second)
        return True
    except Exception as e:
        if e.__cause__:  # should be ValueError
            raise Exception(f'"{second}" does not exist.') from e

        return False