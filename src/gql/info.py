import strawberry

__all__ = (
    'api_version',
)

@strawberry.field(description = "Version number of the API.")
def api_version() -> str:
    return "1.0.0"