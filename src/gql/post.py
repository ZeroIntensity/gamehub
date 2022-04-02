import strawberry
from .permissions import Authenticated, HasAdmin
from strawberry.types import Info
from ..db import Post, PostModel, FoundUser
from typing_extensions import Annotated
import time
from ..utils import make_id, has_post_access

__all__ = (
    'create_post',
    'delete_post',
    'edit_post',
    'can_alter_post'
)

PostID = Annotated[
    str,
    strawberry.argument("ID of the post.")
]
Content = Annotated[
    str,
    strawberry.argument("Content of the post.")
]

@strawberry.field(
    description = "Create a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def create_post(
    info: Info,
    content: Content
) -> Post:
    user: FoundUser = info.context.user
    params: dict = {
        "content": content,
        "author": user.username,
        "epoch": time.time(),
        "id": make_id()
    }

    post = PostModel(**params)
    post.save()

    return Post(**params)  # type: ignore

@strawberry.field(
    description = "Delete a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def delete_post(info: Info, id: PostID) -> str:
    post = has_post_access(id, info.context.user.username)
    post.delete()

    return "Successfully deleted post."

@strawberry.field(
    description = "Check whether a user can alter a post."
)
def can_alter_post(
    id: PostID,
    target: Annotated[
        str,
        strawberry.argument("Account to check permissions on.")
    ]
) -> bool:
    try:
        has_post_access(id, target)
        return True
    except:
        return False

@strawberry.field(
    description = "Edit a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def edit_post(info: Info, id: PostID, content: Content) -> str:
    post = has_post_access(id, info.context.user.username)
    post.content = content
    post.update()

    return "Successfully updated post."