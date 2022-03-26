import strawberry
import re
from ..db import User as UserModel
from typing_extensions import Annotated

@strawberry.input(description = "User authentication data.")
class User:
    name: str = strawberry.field(description = 'Name of the user.')
    password: str = strawberry.field(description = 'Password of the user.')

@strawberry.field(description = "Create a new account.")
def create_account(user: Annotated[User, strawberry.argument("Data to create the account from.")]) -> str:
    if UserModel.find({"username": user.name}):
        raise Exception("user already exists")
    return "Created account"