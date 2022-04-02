import strawberry
from .permissions import Authenticated
from strawberry.types import Info
from ..db import FoundUser
from .games import TargetGame
from ..utils import game_exists

@strawberry.field(
    description = "Like a game.",
    permission_classes = [Authenticated]
)
def like_game(info: Info, name: TargetGame) -> str:
    user: FoundUser = info.context.user
    game = game_exists(name)

    if user.username in game.likes:
        raise Exception("You have already liked this game.")

    game.likes.append(user.username)
    game.update()

    return "Successfully liked game."

@strawberry.field(
    description = "Unlike a game.",
    permission_classes = [Authenticated]
)
def unlike_game(info: Info, name: TargetGame) -> str:
    user: FoundUser = info.context.user
    game = game_exists(name)

    if user.username not in game.likes:
        raise Exception("You have not liked this game.")

    game.likes.remove(user.username)
    game.update()

    return "Successfully unliked game."