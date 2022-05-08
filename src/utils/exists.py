from ..db import (
    FoundUser,
    UserModel,
    FoundGame,
    GameModel,
    FoundPost,
    PostModel,
    games
)
from strawberry.types import Info
from .exception import exception
from .find_username import find_username

__all__ = (
    'exists',
    'game_exists',
    'post_exists'
)

def exists(info: Info, username: str) -> FoundUser:
    """Check if a user exists inside a GraphQL resolver."""

    try:
        target = UserModel(username = find_username(username) or '').find()
    except ValueError as e:
        exception(
            info,
            f'User "{username}" does not exist.',
            404,
            e
        )

    return target

def game_exists(info: Info, name: str) -> FoundGame:
    """Check if a game exists inside a GraphQL resolver."""
    found_name: str = ''

    for game in games.find():
        if game['name'].lower() == name.lower():
            found_name = game['name']

    game = GameModel(name = found_name)

    if not game.exists():
        exception(info, f'Game "{name}" does not exist.', 404)

    return game.find()

def post_exists(info: Info, id: str) -> FoundPost:
    """Check if a post exists inside a GraphQL resolver."""
    post = PostModel(id = id)

    if not post.exists():
        exception(info, 'Could not find post.', 404)

    return post.find()