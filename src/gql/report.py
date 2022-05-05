import strawberry
from discord import Embed
from .permissions import Authenticated
from typing_extensions import Annotated
from strawberry.types import Info
from datetime import datetime
from ..utils import exists, exception, game_exists
from ..db import FoundUser

__all__ = ('issue_report', 'user_report')

@strawberry.field(
    description = "Submit an issue report for a game.",
    permission_classes = [Authenticated]
)
def issue_report(
    info: Info,
    content: Annotated[
        str,
        strawberry.argument("Content of the report.")
    ],
    game: Annotated[
        str,
        strawberry.argument("Name of the game.")
    ]
) -> str:
    user: FoundUser = info.context.user
    game_exists(info, game)

    if len(content) > 400:
        exception(info, "Content cannot be above 400 characters.")

    embed = Embed(
        title = f'Report for game "{game}"',
        description = content,
        color = 0xff5c5c
    )
    embed.set_author(
        name = user.username,
        url = info.context.request.url_for("profile", username = user.username)
    )  # type: ignore
    embed.timestamp = datetime.now()



    return "Successfully submitted issue report."

@strawberry.field(
    description = "Submit a report.",
    permission_classes = [Authenticated]
)
def user_report(
    info: Info,
    content: Annotated[
        str,
        strawberry.argument("Content of the report.")
    ],
    target: Annotated[
        str,
        strawberry.argument("Target user to submit report against.")
    ]
) -> str:
    user: FoundUser = info.context.user

    if len(content) > 300:
        exception(info, "Content cannot be above 300 characters.")

    exists(info, target)
    embed = Embed(
        title = "User Report",
        description = f'**Report on user "{target}"**\n{content}',
        color = 0xff5c5c
    )
    embed.set_author(
        name = user.username,
        url = info.context.request.url_for("profile", username = user.username)
    )  # type: ignore
    embed.timestamp = datetime.now()

    return "Successfully submitted user report."
