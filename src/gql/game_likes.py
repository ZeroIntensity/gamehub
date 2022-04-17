import strawberry
from .permissions import Authenticated
from strawberry.types import Info
from ..db import FoundUser
from .games import TargetGame
from ..utils import game_exists, exception

__all__ = (
    "like_game",
    "unlike_game"
)

@strawberry.field(
    description = "Like a game.",
    permission_classes = [Authenticated]
)
def like_game(info: Info, name: TargetGame) -> str:
    user: FoundUser = info.context.user
    game = game_exists(info, name)

    if user.username in game.likes:
        exception(info, "You have already liked this game.")

    user.likes.append(game.name)
    game.likes.append(user.username)
    game.update()
    user.update()

    return "Successfully liked game."

@strawberry.field(
    description = "Unlike a game.",
    permission_classes = [Authenticated]
)
def unlike_game(info: Info, name: TargetGame) -> str:
    user: FoundUser = info.context.user
    game = game_exists(info, name)

    if user.username not in game.likes:
        exception(info, "You have not liked this game.")

    user.likes.remove(game.name)
    game.likes.remove(user.username)
    game.update()
    user.update()

    return "Successfully unliked game."