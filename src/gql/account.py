import strawberry
import re
from typing_extensions import Annotated
from ..db import UserModel
from argon2 import PasswordHasher
from ..utils import validate

@strawberry.input(description = "User authentication data.")
class User:
    name: str = strawberry.field(description = 'Name of the user.')
    password: str = strawberry.field(description = 'Password of the user.')

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

    hasher = PasswordHasher()
    model.password = hasher.hash(user.password)
    model.save()

    return "Successfully created account."
