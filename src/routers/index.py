from fastapi import APIRouter
from ..utils import template

__all__ = (
    'router',
    'prefix'
)

router = APIRouter()
prefix: str = ''

@router.get('/')
def index():
    return template('index.html')