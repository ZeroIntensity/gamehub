import strawberry
from ..db import games as games_col, posts as posts_col, Game, Post
from typing import List
from ..utils import no_id

__all__ = (
    'games',
    'posts'
)

@strawberry.field(description = "List all games.")
def games() -> List[Game]:
    return [Game(**no_id(game)) for game in games_col.find()]

@strawberry.field(description = "List all posts.")
def posts() -> List[Post]:
    return [Post(**no_id(post)) for post in posts_col.find()]