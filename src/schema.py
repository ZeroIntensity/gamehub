import strawberry
from .gql import *

@strawberry.type(description = "Root type for queries.")
class Query:
    user_data = user_data
    get_game = get_game
    can_access = can_access
    games = games
    posts = posts
    rooms = rooms

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
    edit_comment = edit_comment
    like_game = like_game
    unlike_game = unlike_game
    create_post = create_post
    delete_post = delete_post
    edit_post = edit_post
    login = login
    logout = logout
    suggestion = suggestion
    issue_report = issue_report
    user_report = user_report
    apply = apply
    create_room = create_room
    delete_room = delete_room

schema = strawberry.Schema(Query, mutation = Mutation)
