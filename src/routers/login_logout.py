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
    include_in_schema = False
)
async def logout():
    response = RedirectResponse('/')
    response.delete_cookie('auth')
    return response

@router.get(
    '/login',
    include_in_schema = False
)
async def login(
    request: Request,
    ctx = Depends(ctx_dependency)
):
    if not ctx.user:
        return template('login.html', request, ctx)
    
    return RedirectResponse('/')
