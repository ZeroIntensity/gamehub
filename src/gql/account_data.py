import strawberry
from .account import AccountCredentials, TargetAccount
from ..utils import has_access

@strawberry.type
class User:
    username: str = strawberry.field(
        description = "Account username.",
        name = "name"
    )
    account_type: str = strawberry.field(description = "Account permissions.")

@strawberry.field(description = 'Get data of a user.')
def user_data(
    credentials: AccountCredentials, 
    target: TargetAccount = None
) -> User:
    model_dict = has_access(credentials.name, credentials.password, target) \
        .make_dict()
    
    for i in ['_id', 'password']:
        del model_dict[i]    

    return User(**model_dict)
