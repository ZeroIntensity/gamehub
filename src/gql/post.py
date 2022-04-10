import strawberry
from .permissions import Authenticated, HasAdmin
from strawberry.types import Info
from ..db import Post, PostModel, FoundUser, PostInput
from typing_extensions import Annotated
import time
from ..utils import make_id, has_post_access, validate
import re

__all__ = (
    'create_post',
    'delete_post',
    'edit_post',
    'can_alter_post'
)

def validate_post(info: Info, data: PostInput):
    validate(info, 
    {
        bool(re.match("<.*>", data.content)): "Invalid content.",
        len(data.content) > 300: "Post content cannot exceed 300 characters.",
        len(data.title) > 30: "Post title cannot exceed 30 characters.",
        bool(re.match("<.*>", data.title)): "Invalid title.",
    })

PostID = Annotated[
    str,
    strawberry.argument("ID of the post.")
]
PostData = Annotated[
    PostInput,
    strawberry.argument("Post data.")
]

@strawberry.field(
    description = "Create a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def create_post(
    info: Info,
    data: PostData
) -> Post:
    user: FoundUser = info.context.user

    validate_post(info, data)
    params: dict = {
        "author": user.username,
        "epoch": time.time(),
        "id": make_id(),
        **data.__dict__
    }

    post = PostModel(**params)
    post.save()

    return Post(**params)  # type: ignore

@strawberry.field(
    description = "Delete a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def delete_post(info: Info, id: PostID) -> str:
    post = has_post_access(
        info,
        id,
        info.context.user.username
    )
    post.delete()

    return "Successfully deleted post."

@strawberry.field(
    description = "Check whether a user can alter a post."
)
def can_alter_post(
    info: Info,
    id: PostID,
    target: Annotated[
        str,
        strawberry.argument("Account to check permissions on.")
    ]
) -> bool:
    try:
        has_post_access(info, id, target)
        return True
    except Exception:
        return False

@strawberry.field(
    description = "Edit a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def edit_post(info: Info, id: PostID, data: PostData) -> str:
    post = has_post_access(
        info,
        id,
        info.context.user.username
    )
    validate_post(info, data)

    post.content = data.content
    post.title = data.title
    post.update()

    return "Successfully updated post."