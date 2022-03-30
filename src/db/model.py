from pymongo.collection import Collection
from typing import Union, overload, Literal, TypeVar

__all__ = ['Model']

T = TypeVar("T", bound = "Model")

class Model:
    """Base class representing a model. All classes that derive from this should be dataclasses."""
    
    collection: Collection
    _id: str

    def __init__(self, *_, **__) -> None:
        # to get linters to stop complaining
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        cls.collection = kwargs['collection']
    
    def update(self, data: "Model") -> None:
        """Update the current document."""
        
        if not self._id:
            raise Exception("_id must be present")
        
        self.collection.update_one(
            {
                '_id': self._id
            },
            {
                '$set': data.make_dict()
            }
        )

    def save(self) -> None:
        """Save the current document."""
        self.collection.insert_one(self.make_dict())

    def count(self) -> int:
        """Count of documents based on the current data."""
        return self.collection.count_documents(self.make_dict())

    def exists(self) -> bool:
        """Whether the current document exists."""

        return bool(self.count())

    def make_dict(self) -> dict:
        """Make a dictionary with removed null values from the current data."""
        origin: dict = self.__dict__
        new: dict = {}

        for key, value in origin.items():
            if value is not None: # in case of things like 0, '', etc
                new[key] = value

        return new
    
    def delete(self) -> None:
        """Delete a document based on the current data."""
        self.collection.delete_one(self.make_dict())
    
    @overload
    def find(self: T, return_dict: Literal[False] = False) -> T:
        ...

    @overload
    def find(self, return_dict: Literal[True] = True) -> dict:
        ...

    def find(self: T, return_dict: bool = False) -> Union[dict, T]:
        """Find a document based on the current data."""
        find = self.collection.find_one(self.make_dict())

        if not find:
            raise ValueError("not found")
        
        if not return_dict:
            return self.__class__(**find)

        return find
    
    @classmethod
    def find_by_id(cls, id: str):
        find = cls.collection.find_one({'_id': id})

        if not find:
            raise ValueError("not found")

        return cls(**find)
