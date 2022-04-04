from fastapi import APIRouter, responses, Request
from fastapi.templating import Jinja2Templates
from ..db import posts, PostModel
from typing import List

__all__ = (
    'router',
    'prefix'
)

router = APIRouter()
prefix: str = ''

templates = Jinja2Templates('./templates')

@router.get(
    '/',
    response_class = responses.HTMLResponse
)
async def index(request: Request):
    posts_list: List[PostModel] = [PostModel(**post) for post in posts.find()]

    return templates.TemplateResponse('index.html', {
        'request': request,
        'posts': posts_list
    })