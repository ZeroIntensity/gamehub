from ..utils import (
    game_exists,
    make_id,
    has_access,
    get_comment,
    validate,
    exception
)
import strawberry
from .permissions import Authenticated
from ..db import Comment, FoundUser, ProfileComment
import time
from strawberry.types import Info
from .games import TargetGame
from typing_extensions import Annotated
import bleach
import time

__all__ = (
    "create_comment",
    "delete_comment",
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

def validate_comment(info: Info, content: str):
    # add other things here if you need to
    validate(info, 
    {
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
    game = game_exists(info, name)
    user: FoundUser = info.context.user

    users = [comment['author'] for comment in game.comments]
    
    if users.count(user.username) >= 5:
        exception(info, "You cannot create more than 5 comments on a single game.")

    validate_comment(info, content)
    epoch: float = time.time()
    cleaned: str = bleach.linkify(bleach.clean(content))

    comment = Comment(
        author = user.username,
        content = cleaned,
        epoch = epoch,
        id = make_id(),
        account_type = user.account_type
    )

    user.comments.append({
        'game': game.name,
        'epoch': epoch,
        'content': cleaned
    })
    game.comments.append(comment.__dict__)  # type: ignore
    game.update()
    user.update()

    return comment

@strawberry.field(
    description = "Delete a comment on a game.",
    permission_classes = [Authenticated]
)
def delete_comment(info: Info, data: CommentInput) -> str:
    user: FoundUser = info.context.user

    game = game_exists(info, data.name)
    comment = get_comment(info, data.name, data.id)    

    has_access(info, user, comment["author"])
    game.comments.remove(comment)

    game.update()

    return "Successfully deleted comment."

@strawberry.field(
    description = "Edit a comment on a game.",
    permission_classes = [Authenticated]
)
def edit_comment(info: Info, data: CommentInput, content: Content) -> str:
    user: FoundUser = info.context.user

    game = game_exists(info, data.name)
    comment = get_comment(info, data.name, data.id)
    index: int = game.comments.index(comment)

    if comment["author"] != user.username:
        exception(info, "Only the author can update their comment.", 403)

    validate_comment(info, content)

    game.comments[index]["content"] = bleach.linkify(bleach.clean(content))
    game.update()

    return "Successfully updated comment."