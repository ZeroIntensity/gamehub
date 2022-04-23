import strawberry
from discord import Webhook, RequestsWebhookAdapter, Embed
from .permissions import Authenticated
from typing_extensions import Annotated
from strawberry.types import Info
from datetime import datetime
from ..config import config
from typing import Optional
from ..db import FoundUser

__all__ = ('apply',)

WEBHOOK = Webhook.from_url(
    config.apply_webhook,
    adapter = RequestsWebhookAdapter()
)

@strawberry.input(description = "Object representing an application")
class Application:
    discord_tag: str = strawberry.field(description = "Your discord tag.")
    question_one: bool = strawberry.field(description = "Can you help expand the site to a wider audience?")
    question_two: bool = strawberry.field(description = "Can you help add games to the site?")
    any_other_help: Optional[str] = strawberry.field(description = "Can you help in any other way?", default = None)

@strawberry.field(
    description = "Submit an application.",
    permission_classes = [Authenticated]
)
def apply(
    info: Info,
    content: Annotated[
        Application,
        strawberry.argument("Application data to be sent.")
    ]
) -> str:
    user: FoundUser = info.context.user

    embed = Embed(
        title = "Application",
        color = 0xffa85c
    )
    embed.set_author(
        name = user.username,
        url = info.context.request.url_for("profile", username = user.username)
    )  # type: ignore
    embed.timestamp = datetime.now()

    fields = {
        'Discord Tag': content.discord_tag,
        'Can you help expand the site to a wider audience?': 'Yes' if content.question_one else 'No',
        'Can you help add games to the site?': 'Yes' if content.question_two else 'No',
        'Is there anything else you can help with?': content.any_other_help or 'No'
    }

    for name, value in fields.items():
        embed.add_field(
            name = name,
            value = value,
            inline = False
        )

    WEBHOOK.send(embed = embed)
    return "Successfully submitted application"