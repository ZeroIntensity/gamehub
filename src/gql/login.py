import strawberry
from strawberry.types import Info
from fastapi import Response
from .account import UserInput
from ..config import config
from ..utils import check_creds, sign_jwt
from typing_extensions import Annotated
from .permissions import Authenticated

__all__ = (
    "login",
    "logout"
)

@strawberry.field(description = "Log in to an account.")
def login(
    info: Info,
    credentials: Annotated[
        UserInput,
        strawberry.argument("Account credentials.")
    ]
) -> str:
    response: Response = info.context.response

    if not check_creds(credentials.name, credentials.password):
        raise Exception("Invalid username or password.")

    token: str = sign_jwt(credentials.name)

    response.set_cookie(
        "auth", token,
        secure = config.production,
        samesite = "strict",
        expires = config.auth_validation_time
    )

    return token

@strawberry.field(
    description = "Log out of the current account.",
    permission_classes = [Authenticated]
)
def logout(info: Info) -> str:
    response: Response = info.context.response
    response.delete_cookie("auth")

    return "Successfully logged out."