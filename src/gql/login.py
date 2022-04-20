import strawberry
from strawberry.types import Info
from fastapi import Response
from .account import UserInput
from ..config import config
from ..utils import check_creds, sign_jwt, exception
from typing_extensions import Annotated
from .permissions import Authenticated
from ..db import Termination

__all__ = (
    "login",
    "logout",
    "handle_login"
)

def handle_login(response: Response, username: str, password: str):
    if not check_creds(username, password):
        return False

    token: str = sign_jwt(username)

    response.set_cookie(
        "auth", token,
        secure = config.production,
        samesite = "strict",
        expires = config.auth_validation_time
    )

    return token

@strawberry.field(description = "Log in to an account.")
def login(
    info: Info,
    credentials: Annotated[
        UserInput,
        strawberry.argument("Account credentials.")
    ]
) -> str:
    termination = Termination(username = credentials.name)

    if termination.exists():
        exception(info, f"Account has been terminated: {termination.find().reason}", 410)

    response = handle_login(info.context.response, credentials.name, credentials.password)

    if not response:
        exception(info, "Invalid username or password.")

    return response

@strawberry.field(
    description = "Log out of the current account.",
    permission_classes = [Authenticated]
)
def logout(info: Info) -> str:
    response: Response = info.context.response
    response.delete_cookie("auth")

    return "Successfully logged out."