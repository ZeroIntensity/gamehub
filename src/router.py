from strawberry.fastapi import GraphQLRouter
from strawberry.http import GraphQLHTTPResponse
from strawberry.types import ExecutionResult, Info
from graphql.error.graphql_error import format_error as format_graphql_error

__all__ = (
    "Router",
)

class Router(GraphQLRouter):
    async def process_result(
        self, _, result: ExecutionResult
    ) -> GraphQLHTTPResponse:
        data: GraphQLHTTPResponse = {
            "data": result.data,
            "errors": None
        }

        if result.errors:
            data["errors"] = [format_graphql_error(err) for err in result.errors]

        return data