import strawberry
from discord import Webhook, RequestsWebhookAdapter, Embed
from .permissions import Authenticated
from typing_extensions import Annotated
from strawberry.types import Info
from datetime import datetime
from ..config import config

__all__ = ('suggestion',)

WEBHOOK = Webhook.from_url(
    config.suggest_webhook,
    adapter = RequestsWebhookAdapter()
)

@strawberry.field(
    description = "Submit a suggestion.",
    permission_classes = [Authenticated]
)
def suggestion(
    info: Info,
    content: Annotated[
        str,
        strawberry.argument("Content of the suggestion.")
    ]
) -> str:
    embed = Embed(
        title = "Suggestion",
        description = content,
        color = 0x5caeff
    )
    embed.set_author(name = f'User "{info.context.user.username}"')
    embed.timestamp = datetime.now()

    WEBHOOK.send(embed = embed)
    return "Successfully submitted suggestion."