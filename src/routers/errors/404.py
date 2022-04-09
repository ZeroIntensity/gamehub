from fastapi import Request
from fastapi.templating import Jinja2Templates
from ...utils import nav

__all__ = (
    'error',
    'error'
)

error: int = 404
templates = Jinja2Templates('./templates')

async def handler(request: Request, _):
    return templates.TemplateResponse(
        'error.html',
        {
            'request': request,
            'nav': await nav(None),
            'error': '404',
            'message': 'The requested URL was not found on the server.'
        }, status_code = 404
    )