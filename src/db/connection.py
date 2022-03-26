import pymongo
from ..config import CONFIG

__all__ = (
    "client",
    "db"
)

client = pymongo.MongoClient(CONFIG['mongo_url'])
db = client["gamehub"]