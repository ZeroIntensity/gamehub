import strawberry
from .permissions import Authenticated, HasAdmin
from strawberry.types import Info
from ..db import Post, PostModel, FoundUser, PostInput
from typing_extensions import Annotated
import time
from ..utils import make_id, validate, post_exists
import bleach

__all__ = (
    'create_post',
    'delete_post',
    'edit_post'
)

def validate_post(info: Info, data: PostInput):
    validate(info, 
    {
        len(data.content) > 300: "Post content cannot exceed 300 characters.",
        len(data.title) > 30: "Post title cannot exceed 30 characters.",
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
    post = PostModel(
        author = user.username,
        epoch = time.time(),
        id = make_id(),
        content = bleach.linkify(bleach.clean(data.content)),
        title = bleach.clean(data.title)
    )
    post.save()

    return Post(**post.make_dict())  # type: ignore

@strawberry.field(
    description = "Delete a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def delete_post(info: Info, id: PostID) -> str:
    post = post_exists(info, id)
    post.delete()

    return "Successfully deleted post."

@strawberry.field(
    description = "Edit a post.",
    permission_classes = [Authenticated, HasAdmin]
)
def edit_post(info: Info, id: PostID, data: PostData) -> str:
    post = post_exists(info, id)
    validate_post(info, data)

    post.content = bleach.linkify(bleach.clean(data.content))
    post.title = bleach.clean(data.title)
    post.update()

    return "Successfully updated post."