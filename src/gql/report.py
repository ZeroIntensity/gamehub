import strawberry
from discord import Webhook, RequestsWebhookAdapter, Embed
from .permissions import Authenticated
from typing_extensions import Annotated
from strawberry.types import Info
from datetime import datetime
from ..config import config

__all__ = ('report',)

WEBHOOK = Webhook.from_url(
    config.report_webhook,
    adapter = RequestsWebhookAdapter()
)

@strawberry.field(
    description = "Submit a report.",
    permission_classes = [Authenticated]
)
def report(
    info: Info,
    content: Annotated[
        str,
        strawberry.argument("Content of the report.")
    ]
) -> str:
    embed = Embed(
        title = "Issue Report",
        description = content,
        color = 0xff5c5c
    )
    embed.set_author(name = f'User "{info.context.user.username}"')
    embed.timestamp = datetime.now()

    WEBHOOK.send(embed = embed)
    return "Successfully submitted report."