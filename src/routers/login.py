from fastapi import APIRouter
from ..utils import template

__all__ = (
    'router',
    'prefix'
)

router = APIRouter()
prefix: str = '/login'
# unfinished
@router.post(
    '/',
    response_description = "Successfully logged in.",
    summary = "Log in to an account."
)
def login():
    return {"message": "Successfully logged in."}
