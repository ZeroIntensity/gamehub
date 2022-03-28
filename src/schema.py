import strawberry
from .gql import *

@strawberry.type
class Query:
    api_version = api_version
    user_data = user_data

@strawberry.type
class Mutation:
    create_account = create_account
    promote = promote
    demote = demote
    delete_account = delete_account

schema = strawberry.Schema(Query, mutation = Mutation)
