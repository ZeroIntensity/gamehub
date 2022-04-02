from ..db import FoundUser, UserModel, FoundGame, GameModel

__all__ = (
    'exists',
    'game_exists'
)

def exists(username: str) -> FoundUser:
    """Check if a user exists inside a GraphQL resolver."""

    try:
        target = UserModel(username = username).find()
    except ValueError as e:
        raise Exception(f'User "{username}" does not exist.') from e

    return target

def game_exists(name: str) -> FoundGame:
    game = GameModel(name = name)

    if not game.exists():
        raise Exception(f'"{name}" does not exist.')

    return game.find()