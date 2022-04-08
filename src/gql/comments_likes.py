from ..utils import (
    game_exists,
    make_id,
    has_access,
    get_comment,
    validate
)
import strawberry
from .permissions import Authenticated
from ..db import Comment, FoundUser
import time
from strawberry.types import Info
from .games import TargetGame
from typing_extensions import Annotated
import re

__all__ = (
    "create_comment",
    "delete_comment",
    "like_comment",
    "unlike_comment",
    "edit_comment"
)

Content = Annotated[
   str,
   strawberry.argument("Content of the comment.") 
]
CommentID = Annotated[
    str,
    strawberry.argument("ID of a comment on a game.")
]

def validate_comment(content: str):
    validate({
        bool(re.match("<.*>", content)): "Invalid content.",
        len(content) > 300: "Comment content cannot exceed 300 characters."
    })

@strawberry.input(description = "Comment lookup data.")
class CommentData:
    id: str = strawberry.field(description = "ID of a comment on a game.")
    name: str = strawberry.field(description = "Name of the game.")

CommentInput = Annotated[
    CommentData,
    strawberry.argument("Data to lookup the comment with.")
]

@strawberry.field(
    description = "Post a comment on a game.",
    permission_classes = [Authenticated]
)
def create_comment(info: Info, name: TargetGame, content: Content) -> Comment:
    game = game_exists(name)
    
    validate_comment(content)
    comment = Comment(
        author = info.context.user.username,
        likes = [],
        content = content,
        epoch = time.time(),
        id = make_id()
    )

    game.comments.append(comment.__dict__)  # type: ignore
    game.update()

    return comment

@strawberry.field(
    description = "Delete a comment on a game.",
    permission_classes = [Authenticated]
)
def delete_comment(info: Info, data: CommentInput) -> str:
    user: FoundUser = info.context.user

    game = game_exists(data.name)
    comment = get_comment(data.name, data.id)    

    has_access(user, comment["author"])
    game.comments.remove(comment)

    game.update()

    return "Successfully deleted comment."

@strawberry.field(
    description = "Like a comment on a game.",
    permission_classes = [Authenticated]
)
def like_comment(info: Info, data: CommentInput) -> str:
    user: FoundUser = info.context.user

    game = game_exists(data.name)
    comment = get_comment(data.name, data.id)
    index: int = game.comments.index(comment)

    if user.username in comment['likes']:
        raise Exception('You have already liked this comment.')

    comment["likes"].append(user.username)
    game.comments[index] = comment

    game.update()

    return "Successfully liked comment."

@strawberry.field(
    description = "Unlike a comment on a game.",
    permission_classes = [Authenticated]
)
def unlike_comment(info: Info, data: CommentInput) -> str:
    # TODO: move this into a seperate function
    user: FoundUser = info.context.user

    game = game_exists(data.name)
    comment = get_comment(data.name, data.id)
    index: int = game.comments.index(comment)

    if user.username not in comment['likes']:
        raise Exception('You have not liked this comment.')

    game.comments[index]["likes"].remove(user.username)
    game.update()

    return "Successfully unliked comment."

@strawberry.field(
    description = "Edit a comment on a game.",
    permission_classes = [Authenticated]
)
def edit_comment(info: Info, data: CommentInput, content: Content) -> str:
    user: FoundUser = info.context.user

    game = game_exists(data.name)
    comment = get_comment(data.name, data.id)
    index: int = game.comments.index(comment)

    if comment["author"] != user.username:
        raise Exception("Only the author can update their comment.")

    validate_comment(content)

    game.comments[index]["content"] = content
    game.update()

    return "Successfully updated comment."