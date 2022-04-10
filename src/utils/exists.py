from ..db import (
    FoundUser,
    UserModel,
    FoundGame,
    GameModel,
    FoundPost,
    PostModel
)
from strawberry.types import Info
from .exception import exception

__all__ = (
    'exists',
    'game_exists',
    'post_exists'
)

def exists(info: Info, username: str) -> FoundUser:
    """Check if a user exists inside a GraphQL resolver."""

    try:
        target = UserModel(username = username).find()
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
    game = GameModel(name = name)

    if not game.exists():
        exception(info, f'Game "{name}" does not exist.', 404)

    return game.find()

def post_exists(info: Info, id: str) -> FoundPost:
    """Check if a post exists inside a GraphQL resolver."""
    post = PostModel(id = id)

    if not post.exists():
        exception(info, 'Could not find post.', 404)

    return post.find()