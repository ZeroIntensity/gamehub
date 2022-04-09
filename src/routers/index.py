from fastapi import APIRouter, responses, Request, Depends
from fastapi.templating import Jinja2Templates
from ..db import posts, PostModel
from typing import List
from ..gql import ctx_dependency
from ..utils import nav

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
async def index(request: Request, ctx = Depends(ctx_dependency)):
    posts_list: List[PostModel] = [PostModel(**post) for post in posts.find()]
    return templates.TemplateResponse('index.html', {
        'request': request,
        'posts': reversed(posts_list),
        'user': ctx.user,
        'nav': await nav(ctx.user)
    })