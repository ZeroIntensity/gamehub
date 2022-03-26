import strawberry
from strawberry.schema.config import StrawberryConfig
from .gql import *

@strawberry.type
class Query:
    api_version = api_version
    create_account = create_account
    

schema = strawberry.Schema(Query)