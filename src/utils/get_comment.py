from .exists import game_exists
from typing import Optional
from .._typing import Comment
from .exception import exception
from strawberry.types import Info

__all__ = ('get_comment',)

def get_comment(info: Info, name: str, id: str) -> Comment:
    """Fetch a comment from a game."""
    game = game_exists(info, name)    
    target: Optional[Comment] = None

    for comment in game.comments:
        if comment["id"] == id:
            target = comment
    
    if not target:
        exception(info, "Could not find comment.", 404)

    return target