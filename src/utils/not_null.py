from typing import TypeVar, Optional

T = TypeVar("T")

def not_null(value: Optional[T]) -> T:
    """Assert a value is not null."""
    assert value is not None
    return value
