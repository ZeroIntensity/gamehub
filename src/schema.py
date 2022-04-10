import strawberry
from .gql import *

@strawberry.type(description = "Root type for queries.")
class Query:
    user_data = user_data
    get_game = get_game
    can_access = can_access
    can_alter_post = can_alter_post
    games = games
    posts = posts

@strawberry.type(description = "Root type for mutations.")
class Mutation:
    create_account = create_account
    promote = promote
    demote = demote
    delete_account = delete_account
    create_game = create_game
    delete_game = delete_game
    create_comment = create_comment
    delete_comment = delete_comment
    like_comment = like_comment
    unlike_comment = unlike_comment
    edit_comment = edit_comment
    like_game = like_game
    unlike_game = unlike_game
    create_post = create_post
    delete_post = delete_post
    edit_post = edit_post
    login = login
    logout = logout

schema = strawberry.Schema(Query, mutation = Mutation)
