from fastapi import Request
from fastapi.templating import Jinja2Templates
from ...utils import nav

__all__ = (
    'error',
    'error'
)

error: int = 405
templates = Jinja2Templates('./templates')

async def handler(request: Request, _):
    return templates.TemplateResponse(
        'error.html',
        {
            'request': request,
            'nav': await nav(None),
            'error': '405',
            'message': 'The method you used is not supported.'
        }, status_code = 405
    )