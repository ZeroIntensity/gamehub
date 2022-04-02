from .exists import game_exists
from typing import Optional
from .._typing import Comment

__all__ = ['get_comment']

def get_comment(name: str, id: str) -> Comment:
    game = game_exists(name)    
    target: Optional[Comment] = None

    for comment in game.comments:
        if comment["id"] == id:
            target = comment
    
    if not target:
        raise Exception("Could not find comment.")

    return target