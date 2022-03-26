from src.app import app
import uvicorn
import json
from src.config import CONFIG

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host = CONFIG['host'], 
        port = CONFIG['port'],
        reload = CONFIG['reload']
    )