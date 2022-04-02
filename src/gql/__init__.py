"""Module holding all GraphQL resolvers."""

from .info import *
from .account import create_account, promote, demote, delete_account
from .account_data import user_data
from .permissions import get_context, Authenticated
from .games import get_game, create_game, delete_game
from .comments_likes import comment_on_game, delete_comment