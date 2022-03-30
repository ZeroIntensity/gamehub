import strawberry
from .account import AccountCredentials, TargetAccount
from ..utils import has_access

@strawberry.type
class User:
    name: str
    account_type: str

@strawberry.field(description = 'Get data of a user.')
def user_data(
    credentials: AccountCredentials, 
    target: TargetAccount = None
) -> User:
    model = has_access(credentials.name, credentials.password, target)

    assert model.username
    assert model.account_type

    return User(name = model.username, account_type = model.account_type)