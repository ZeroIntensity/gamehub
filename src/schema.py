import strawberry
from .gql import *

@strawberry.type
class Query:
    api_version = api_version
    user_data = user_data
    get_game = get_game

@strawberry.type
class Mutation:
    create_account = create_account
    promote = promote
    demote = demote
    delete_account = delete_account
    create_game = create_game
    delete_game = delete_game

schema = strawberry.Schema(Query, mutation = Mutation)
