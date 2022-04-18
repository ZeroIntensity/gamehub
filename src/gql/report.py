import strawberry
from discord import Webhook, RequestsWebhookAdapter, Embed
from .permissions import Authenticated
from typing_extensions import Annotated
from strawberry.types import Info
from datetime import datetime
from ..config import config
from ..utils import exists
from ..db import FoundUser

__all__ = ('issue_report', 'user_report')

WEBHOOK = Webhook.from_url(
    config.report_webhook,
    adapter = RequestsWebhookAdapter()
)

@strawberry.field(
    description = "Submit an issue report.",
    permission_classes = [Authenticated]
)
def issue_report(
    info: Info,
    content: Annotated[
        str,
        strawberry.argument("Content of the report.")
    ]
) -> str:
    user: FoundUser = info.context.user

    embed = Embed(
        title = "Issue Report",
        description = content,
        color = 0xff5c5c
    )
    embed.set_author(
        name = user.username,
        url = info.context.request.url_for("profile", username = user.username)
    )  # type: ignore
    embed.timestamp = datetime.now()

    WEBHOOK.send(embed = embed)
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

    WEBHOOK.send(embed = embed)
    return "Successfully submitted user report."