from ..utils import game_exists, make_id, has_access
import strawberry
from .permissions import Authenticated
from ..db import Comment, GameModel, FoundUser
import time
from strawberry.types import Info
from .games import TargetGame
from typing_extensions import Annotated
from typing import Optional
from .._typing import Comment as CommentType

Content = Annotated[
   str,
   strawberry.argument("Content of the comment.") 
]

@strawberry.field(
    description = "Post a comment on a game.",
    permission_classes = [Authenticated]
)
def comment_on_game(info: Info, name: TargetGame, content: Content) -> Comment:
    game = game_exists(name)

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
def delete_comment(info: Info, name: TargetGame, id: str) -> str:
    user: FoundUser = info.context.user
    game = game_exists(name)
    
    target: Optional[CommentType] = None

    for comment in game.comments:
        if comment["id"] == id:
            target = comment
    
    if not target:
        raise Exception("Could not find comment.")

    has_access(user, target["author"])
    game.comments.remove(target)

    game.update()

    return "Successfully deleted comment."
