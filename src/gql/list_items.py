import strawberry
from ..db import (
    games as games_col,
    posts as posts_col,
    Game,
    Post,
    Comment
)
from typing import List, Dict
from ..utils import no_id

__all__ = (
    'games',
    'posts',
    'get_games'
)

def get_games() -> List[Game]:
    res: List[Game] = []

    for game in games_col.find():
        params: dict = no_id(game)
        comments: List[Comment] = [
            Comment(**comment) for comment in params['comments']
        ]

        params['comments'] = comments
        res.append(Game(**params))

    return sorted(res, key = lambda x: x.likes, reverse = True)

@strawberry.field(description = "List all games.")
def games() -> List[Game]:
    return get_games()

@strawberry.field(description = "List all posts.")
def posts() -> List[Post]:
    return [Post(**no_id(post)) for post in posts_col.find()]