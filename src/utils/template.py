from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Any, Optional
from .nav import nav
from ..db import FoundUser
from ..gql import Context

templates = Jinja2Templates('./templates')

__all__ = ("template",)

def template(name: str, request: Request, ctx: Context, **kwargs: Any):
    """Return an HTML template."""

    user: Optional[FoundUser] = ctx.user

    params: dict = {
        'request': request,
        'user': user,
        'nav': nav(user)
    }

    return templates.TemplateResponse(name, {**params, **kwargs})

