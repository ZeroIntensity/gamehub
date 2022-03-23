import json
from ._typing import Config, AppConfig

with open('./config.json') as f:
    config: Config = json.load(f)

state_config: AppConfig = config['prod' if config['production'] else 'dev']