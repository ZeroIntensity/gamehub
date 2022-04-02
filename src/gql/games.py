import strawberry
from ..db import GameModel, GameInput, Game, Comment
from .permissions import Authenticated, HasAdmin
from ..utils import game_exists
from typing_extensions import Annotated
from typing import List

TargetGame = Annotated[
    str,
    strawberry.argument("Name of the game.")
]

@strawberry.field(
    description = "Create a game.",
    permission_classes = [Authenticated, HasAdmin]
)
def create_game(data: GameInput) -> str:
    model = GameModel(name = data.name)

    if model.exists():
        raise Exception(f'Game "{data.name}" already exists.')
    

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
def delete_game(name: TargetGame) -> str:
    game = game_exists(name)
    game.delete()
    return f'Successfully deleted "{game}"'

@strawberry.field(description = "Get game data.")
def get_game(name: TargetGame) -> Game:
    game = game_exists(name)
    params = game.make_dict()

    del params['_id']

    comments: List[Comment] = [
        Comment(**comment) for comment in params['comments']
    ]

    del params['comments']

    return Game(**params, comments = comments)