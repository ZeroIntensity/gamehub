from fastapi import APIRouter, HTTPException, Request, Depends
from ..gql import ctx_dependency
from ..utils.template import template
from ..db import GameModel

prefix: str = '/games'
router = APIRouter()

@router.get(
    '/play/{name}',
    include_in_schema = False
)
async def suggestions(name: str, request: Request, ctx = Depends(ctx_dependency)):
    game = GameModel(name = name)

    if not game.exists():
        raise HTTPException(404, "Game not found.")

    return template(
        "play.html",
        request,
        ctx,
        game = game.find()
    )
