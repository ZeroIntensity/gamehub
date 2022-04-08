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
    production: bool
    auth_validation_time: int

_reload = os.environ.get('RELOAD')

config = Config(**{
    'port': int(os.environ.get('PORT') or 5000),
    'host': os.environ.get('HOST') or 'localhost',
    'reload': _reload if _reload is not None else True,
    'mongo_port': os.environ.get('MONGO_PORT') or 27017,
    'mongo_host': os.environ.get('MONGO_HOST') or 'localhost',
    'production': bool(os.environ.get('PRODUCTION')),
    'auth_validation_time': os.environ.get('AUTH_VALIDATION_TIME') or 600
})

