from fastapi import APIRouter, Path, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from ..utils.template import template
from ..gql import ctx_dependency
from ..db import UserModel, Termination
from ..utils import check_perms_bool

prefix: str = '/profile'
router = APIRouter()

@router.get(
    '/{username}',
    include_in_schema = False
)
async def profile(
    request: Request,
    username: str = Path(..., title = "The account to find."),
    ctx = Depends(ctx_dependency)
):
    if username == "me":
        if not ctx.user:
            return RedirectResponse("/login")
        
        username = ctx.user.username 

    if Termination(username = username).exists():
        return template(
            "terminated.html",
            request,
            ctx,
            username = username
        )

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
