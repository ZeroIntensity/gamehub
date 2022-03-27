from pymongo.collection import Collection

__all__ = ['Model']

class Model:
    """Base class representing a model. All classes that derive from this should be dataclasses."""
    
    collection: Collection
    
    def __init_subclass__(cls, **kwargs) -> None:
        cls.collection = kwargs['collection']

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

