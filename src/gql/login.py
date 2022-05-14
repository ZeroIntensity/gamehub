import strawberry
from strawberry.types import Info
from fastapi import Response
from .account import UserInput
from ..config import config
from ..utils import (
    check_creds,
    sign_jwt,
    exception
)
from typing_extensions import Annotated
from .permissions import Authenticated
from ..db import Termination

__all__ = (
    "login",
    "logout",
)

@strawberry.field(description = "Log in to an account.")
def login(
    info: Info,
    credentials: Annotated[
        UserInput,
        strawberry.argument("Account credentials.")
    ]
) -> str:
    termination = Termination(username = credentials.name.lower())

    if termination.exists():
        exception(info, f"Account has been terminated: {termination.find().reason}", 410)

    if not check_creds(credentials.name, credentials.password):
        exception(info, "Invalid username or password.")

    token: str = sign_jwt(credentials.name)

    info.context.response.set_cookie(
        "auth", token,
        secure = config.production,
        samesite = "lax",
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
