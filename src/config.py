import os
from dataclasses import dataclass

__all__ = ['config']

@dataclass
class Config:
    port: int
    host: str
    reload: bool
    mongo_port: str
    mongo_host: str


config = Config(**{
    'port': int(os.environ.get('PORT') or 5000),
    'host': os.environ.get('HOST') or 'localhost',
    'reload': bool(os.environ.get('RELOAD')) or True,
    'mongo_port': os.environ.get('MONGO_PORT') or 27017,
    'mongo_host': os.environ.get('MONGO_HOST') or 'localhost'
})

