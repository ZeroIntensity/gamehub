import strawberry
from .gql import api_version

@strawberry.type
class Query:
    api_version = strawberry.field(resolver = api_version)

schema = strawberry.Schema(Query)