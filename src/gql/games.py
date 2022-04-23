import strawberry
from ..db import GameModel, GameInput, Game, Comment
from .permissions import Authenticated, HasAdmin
from ..utils import game_exists, exception, exists
from typing_extensions import Annotated
from typing import List
from strawberry.types import Info
from contextlib import suppress

TargetGame = Annotated[
    str,
    strawberry.argument("Name of the game.")
]

__all__ = (
    "TargetGame",
    "create_game",
    "delete_game",
    "get_game"
)

@strawberry.field(
    description = "Create a game.",
    permission_classes = [Authenticated, HasAdmin]
)
def create_game(
    info: Info,
    data: Annotated[
        GameInput,
        strawberry.argument("Data to create game from.")
    ]
) -> str:
    model = GameModel(name = data.name)

    if model.exists():
        exception(info, f'Game "{data.name}" already exists.')
    
    params = {
        'data': data.data,
        'likes': [],
        'comments': []
    }

    for key, value in params.items():
        setattr(model, key, value)

    model.save()

    return f'Created game "{data.name}"'

@strawberry.field(
    description = "Delete a game.",
    permission_classes = [Authenticated, HasAdmin]
)
def delete_game(info: Info, name: TargetGame) -> str:
    game = game_exists(info, name)

    likes: list = game.likes
    comments: list = game.comments

    for username in likes:
        try:
            user = exists(info, username)
        except Exception:
            continue
        
        user.likes.remove(name)
        user.update()

    for comment in comments:
        try:
            user = exists(info, comment['author'])
        except Exception:
            continue
        
        for profile_comment in user.comments:
            if profile_comment['game'] == name:
                user.comments.remove(profile_comment)

        user.update()

    game.delete()

    return f'Successfully deleted "{game}"'

@strawberry.field(description = "Get game data.")
def get_game(info: Info, name: TargetGame) -> Game:
    game = game_exists(info, name)
    params = game.make_dict()

    del params['_id']

    comments: List[Comment] = [
        Comment(**comment) for comment in params['comments']
    ]

    del params['comments']

    return Game(**params, comments = comments)