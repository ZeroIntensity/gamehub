def no_id(data: dict) -> dict:
    """Remove the _id key from a dictionary."""
    del data["_id"]
    return data