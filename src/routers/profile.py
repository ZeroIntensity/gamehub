from fastapi import APIRouter, Path, Request, Depends, HTTPException
from ..utils.template import template
from ..gql import ctx_dependency
from ..db import UserModel

prefix: str = '/profile'
router = APIRouter()

@router.get('/{name}')
async def profile(
    request: Request,
    name: str = Path(..., title = "The account to find."),
    ctx = Depends(ctx_dependency)
):
    
    try:
        user = UserModel(username = name).find()
    except ValueError as e:
        raise HTTPException(status_code = 404, detail = "User Not Found") from e

    return template("profile.html", request, ctx, account = user)
