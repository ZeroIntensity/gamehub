import pymongo
from ..config import config

__all__ = (
    'db',
    'users',
    'games',
    'posts',
    'terminations'
)

client = pymongo.MongoClient(
    config.mongo_host,
    config.mongo_port,
    **{
        'username': config.mongo_username,
        'password': config.mongo_password,
        'authMechanism': 'SCRAM-SHA-256'
    } if config.mongo_auth else {}
)
db = client.gamehub

users = db.users
games = db.games
posts = db.posts
terminations = db.terminations