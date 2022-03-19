from fastapi import APIRouter

__all__ = (
    'router',
    'prefix'
)

router = APIRouter()
prefix: str = ''

@router.get('/')
def index():
    return {'hello': 'world'}