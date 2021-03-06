"""Module holding all GraphQL resolvers."""

from .account import create_account, promote, demote, delete_account
from .account_data import user_data, can_access
from .permissions import (
    get_context,
    Authenticated,
    HasAdmin,
    ctx_dependency, 
    Context
)
from .games import get_game, create_game, delete_game
from .comments import (
    create_comment,
    delete_comment,
    edit_comment
)
from .game_likes import like_game, unlike_game
from .post import create_post, delete_post, edit_post
from .list_items import (
    games,
    posts,
    get_games,
    transform_comments,
    rooms,
    get_rooms
)
from .login import login, logout
from .suggestions import suggestion
from .report import issue_report, user_report
from .apply import apply
from .chatrooms import create_room, delete_room