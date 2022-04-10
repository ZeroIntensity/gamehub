import strawberry
from ..db import GameModel, GameInput, Game, Comment
from .permissions import Authenticated, HasAdmin
from ..utils import game_exists, exception
from typing_extensions import Annotated
from typing import List
from strawberry.types import Info

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
def create_game(info: Info, data: GameInput) -> str:
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