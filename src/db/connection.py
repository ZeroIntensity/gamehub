import pymongo
from ..config import config

__all__ = (
    'db',
    'users',
    'games',
    'posts'
)

client = pymongo.MongoClient(config.mongo_host, config.mongo_port)
db = client.gamehub

users = db.users
games = db.games
posts = db.posts
