from fastapi import Request
from fastapi.templating import Jinja2Templates
from ...utils import nav

__all__ = (
    'error',
    'error'
)

error: int = 503
templates = Jinja2Templates('./templates')

async def handler(request: Request, _):
    return templates.TemplateResponse(
        'error.html',
        {
            'request': request,
            'nav': await nav(None),
            'error': '503',
            'message': 'GameHub is currently unavailable, sorry for the inconvenience.'
        }, status_code = 503
    )