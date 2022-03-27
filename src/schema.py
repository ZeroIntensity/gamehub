import strawberry
from .gql import *

@strawberry.type
class Query:
    api_version = api_version

@strawberry.type
class Mutation:
    create_account = create_account
    promote = promote
    demote = demote

schema = strawberry.Schema(Query, mutation = Mutation)
