from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod
from typing import Optional

__all__ = ['Model']

class Model(ABC):
    """Abstract class representing a database document."""

    @abstractmethod
    def __init__(self, _id: Optional[str], *args, **kwargs) -> None:
        ...

    @abstractmethod
    def create(self) -> str:
        """Create a new database document based on the current value."""
        ...

    @abstractmethod
    def delete(self) -> None:
        """Deleting the current database document."""
        ...
    
    @abstractproperty
    def is_real(self) -> bool:
        """Whether the current object is a real database document."""
        ...

    @is_real.setter
    def is_real(self, value: bool) -> None:
        ...

    @abstractclassmethod
    def find(cls, values: dict):
        """Find an existing document based on the given values."""
        ...

    @abstractmethod
    def as_dict(self) -> dict:
        """Returns a dictionary representation of the given values."""
        ...

    @abstractproperty
    def document_id(self) -> Optional[str]:
        ...