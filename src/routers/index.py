from fastapi import APIRouter, responses
from ..utils import template

__all__ = (
    'router',
    'prefix'
)

router = APIRouter()
prefix: str = ''

@router.get(
    '/',
    response_class = responses.HTMLResponse
)
def index():
    return template('index.html')