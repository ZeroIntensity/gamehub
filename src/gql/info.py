import strawberry

@strawberry.field(description = "Version number of the API.")
def api_version() -> str:
    return "0.0.1"