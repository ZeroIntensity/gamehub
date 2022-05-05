import os
from dataclasses import dataclass
from dotenv import load_dotenv

__all__ = ['config']

load_dotenv()
VERSION: str = '1.0.0'

@dataclass
class Config:
    port: int
    host: str
    reload: bool
    mongo_port: str
    mongo_host: str
    production: bool
    auth_validation_time: int
    version: str
    suggest_webhook: str
    report_webhook: str
    apply_webhook: str
    mongo_username: str
    mongo_password: str
    mongo_auth: bool
    ssl: bool

_reload = os.environ.get('RELOAD')

config = Config(**{
    'port': int(os.environ.get('PORT') or 5000),
    'host': os.environ.get('HOST') or 'localhost',
    'reload': _reload if _reload is not None else True,
    'mongo_port': os.environ.get('MONGO_PORT') or 27017,
    'mongo_host': os.environ.get('MONGO_HOST') or 'localhost',
    'production': bool(os.environ.get('PRODUCTION')),
    'auth_validation_time': os.environ.get('AUTH_VALIDATION_TIME') or 2628000,
    'version': os.environ.get('VERSION') or VERSION,
    'suggest_webhook': os.environ['SUGGEST_WEBHOOK'],
    'report_webhook': os.environ['REPORT_WEBHOOK'],
    'apply_webhook': os.environ['APPLY_WEBHOOK'],
    'mongo_username': os.environ.get('MONGO_USERNAME') or '',
    'mongo_password': os.environ.get('MONGO_PASSWORD') or '',
    'mongo_auth': bool(os.environ.get('MONGO_AUTH')),
    'ssl': bool(os.environ.get('SSL'))
})

