from src.app import app
import uvicorn
import json
from src.config import state_config as conf

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host = conf['ip'], 
        port = conf['port'], 
        **conf['extra']
    )