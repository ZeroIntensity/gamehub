import uvicorn
from src.config import config
from src.app import app
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if config.ssl:
    app.add_middleware(HTTPSRedirectMiddleware)

if __name__ == '__main__':
    if not config.production:
        uvicorn.run(
            'main:app', 
            host = config.host, 
            port = config.port,
            reload = config.reload
        )
