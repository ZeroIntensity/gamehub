import strawberry
from ..db import (
    games as games_col,
    posts as posts_col,
    Game,
    Post,
    Comment,
    Termination,
    chatrooms,
    Room
)
from typing import List
from ..utils import no_id
from .._typing import Comment as CommentType

__all__ = (
    'games',
    'posts',
    'get_games',
    'transform_comments',
    'rooms',
    'get_rooms'
)

TERMINATED_COMMENT = lambda epoch, id, author: {
    "author": author,
    "content": "This comment is from a deleted account.",
    "epoch": epoch,
    "account_type": "user",
    "id": id,
    "terminated": True
}

no_term = lambda x: {**x, "terminated": False}

def transform_comments(comments: List[CommentType]) -> List[Comment]:
    return [
            Comment(
                **no_term(comment) if not Termination(
                    username = comment['author'].lower()
                ).exists() else TERMINATED_COMMENT(
                    comment["epoch"],
                    comment["id"],
                    comment["author"]
                )
            ) for comment in comments
        ]

def get_games() -> List[Game]:
    res: List[Game] = []

    for game in games_col.find():
        params: dict = no_id(game)
        params['comments'] = transform_comments(params['comments'])
        res.append(Game(**params))

    return sorted(res, key = lambda x: len(x.likes), reverse = True)

def get_rooms() -> List[Room]:
    return [Room(**no_id(room)) for room in chatrooms.find()]

@strawberry.field(description = "Get all games.")
def games() -> List[Game]:
    return get_games()

@strawberry.field(description = "Get all posts.")
def posts() -> List[Post]:
    return [Post(**no_id(post)) for post in posts_col.find()]

@strawberry.field(description = "Get all chatrooms.")
def rooms() -> List[Room]:
    return get_rooms()