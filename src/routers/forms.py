from fastapi import APIRouter, Request, Depends
from ..gql import ctx_dependency
from ..utils.template import template

prefix: str = ''
router = APIRouter()

@router.get(
    '/applications',
    include_in_schema = False
)
async def apply(request: Request, ctx = Depends(ctx_dependency)):
    return template(
        'apply.html',
        request,
        ctx
    )

@router.get(
    '/report',
    include_in_schema = False
)
async def report(request: Request, ctx = Depends(ctx_dependency)):
    return template(
        'report.html',
        request,
        ctx
    )

@router.get(
    '/suggestions',
    include_in_schema = False
)
async def suggestions(request: Request, ctx = Depends(ctx_dependency)):
    return template(
        'suggestions.html',
        request,
        ctx
    )

