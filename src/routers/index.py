from fastapi import APIRouter, responses, Request, Depends, Response
from fastapi.responses import FileResponse
from ..db import posts, PostModel
from typing import List
from ..gql import ctx_dependency, get_games
from ..utils.template import template  # circular dependency issues

__all__ = (
    'router',
    'prefix'
)

router = APIRouter()
prefix: str = ''

@router.get(
    '/',
    response_class = responses.HTMLResponse,
    summary = 'Get the home page.'
)
async def index(request: Request, ctx = Depends(ctx_dependency)):
    posts_list: List[PostModel] = [PostModel(**post) for post in posts.find()]
    
    return template(
        'index.html',
        request,
        ctx,
        posts = reversed(posts_list)
    )

def liked(name: str, likes: list):
    return name in likes

@router.get(
    '/games',
    response_class = responses.HTMLResponse,
    summary = "Get the games page."
)
async def games(request: Request, ctx = Depends(ctx_dependency)):
    return template(
        'games.html',
        request,
        ctx,
        games = get_games(),
        len = len,
        liked = liked
    )

@router.get('/favicon.ico')
def favicon():
    return FileResponse('./static/assets/favicon.ico')