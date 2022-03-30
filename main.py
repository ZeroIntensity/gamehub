import uvicorn
from src.config import config
from src.app import app

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host = config.host, 
        port = config.port,
        reload = config.reload
    )
