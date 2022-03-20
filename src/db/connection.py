import pymongo
from ..config import state_config

__all__ = (
    "client",
    "db"
)

client = pymongo.MongoClient(state_config['mongo_url'])
db = client["gamehub"]