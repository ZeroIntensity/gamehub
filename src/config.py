import json
from typing import TypedDict

class AppConfig(TypedDict):
    ip: str
    port: int
    extra: dict
    mongo_url: str

class Config(TypedDict):
    production: bool
    prod: AppConfig
    dev: AppConfig

with open('./config.json') as f:
    config: Config = json.load(f)

state_config: AppConfig = config['prod' if config['production'] else 'dev']