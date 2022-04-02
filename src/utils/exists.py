from ..db import (
    FoundUser,
    UserModel,
    FoundGame,
    GameModel,
    FoundPost,
    PostModel
)

__all__ = (
    'exists',
    'game_exists',
    'post_exists'
)

def exists(username: str) -> FoundUser:
    """Check if a user exists inside a GraphQL resolver."""

    try:
        target = UserModel(username = username).find()
    except ValueError as e:
        raise Exception(f'User "{username}" does not exist.') from e

    return target

def game_exists(name: str) -> FoundGame:
    """Check if a game exists inside a GraphQL resolver."""
    game = GameModel(name = name)

    if not game.exists():
        raise Exception(f'Game "{name}" does not exist.')

    return game.find()

def post_exists(id: str) -> FoundPost:
    """Check if a post exists inside a GraphQL resolver."""
    post = PostModel(id = id)

    if not post.exists():
        raise Exception('Could not find post.')

    return post.find()