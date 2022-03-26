from ._typing import Config
import os

__all__ = ['CONFIG']

CONFIG: Config = {
    'port': int(os.environ.get('PORT') or 5000),
    'host': os.environ.get('HOST') or 'localhost',
    'reload': bool(os.environ.get('RELOAD')) or True,
    'mongo_url': os.environ.get('MONGO_URL') or 'mongodb://0.0.0.0:27017/'
}