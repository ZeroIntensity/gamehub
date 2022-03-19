from src.app import app
import uvicorn
import json

with open('./config.json') as f:
    config = json.load(f)

conf = config['prod' if config['production'] else 'dev']

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host = conf['ip'], 
        port = conf['port'], 
        **conf['extra']
    )