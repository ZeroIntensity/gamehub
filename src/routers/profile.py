from fastapi import APIRouter, Path, Request, Depends, HTTPException
from ..utils.template import template
from ..gql import ctx_dependency
from ..db import UserModel
from ..utils import check_perms_bool

prefix: str = '/profile'
router = APIRouter()

@router.get('/{username}')
async def profile(
    request: Request,
    username: str = Path(..., title = "The account to find."),
    ctx = Depends(ctx_dependency)
):
    
    try:
        user = UserModel(username = username).find()
    except ValueError as e:
        raise HTTPException(status_code = 404, detail = "User Not Found") from e

    return template(
        "profile.html",
        request,
        ctx,
        account = user,
        has_access = check_perms_bool
    )
