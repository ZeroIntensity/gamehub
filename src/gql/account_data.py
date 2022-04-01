import strawberry
from ..db import FoundUser
from .account import TargetAccount
from ..utils import has_access
from strawberry.types import Info

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
