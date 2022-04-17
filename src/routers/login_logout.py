from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from ..utils.template import template
from ..gql import ctx_dependency

router = APIRouter()
prefix: str = ''

class UserPasswordInput(BaseModel):
    username: str
    password: str

@router.get(
    '/logout',
    response_class = RedirectResponse,
    status_code = 307,
    summary = "Log out of the current account.",
    response_description = "Redirected to the home page.",
)
async def logout():
    response = RedirectResponse('/')
    response.delete_cookie('auth')
    return response

@router.get(
    '/login',
)
async def login(
    request: Request,
    ctx = Depends(ctx_dependency)
):
    if not ctx.user:
        return template('login.html', request, ctx)
    
    return RedirectResponse('/')
