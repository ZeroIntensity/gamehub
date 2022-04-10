from fastapi import Response, APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()
prefix: str = ''

@router.get(
    '/logout',
    response_class = RedirectResponse,
    status_code = 307,
    summary = "Log out of the current account.",
    response_description = "Redirected to the next resource.",
)
async def logout(response: Response, next: str = '/'):
    response.delete_cookie('auth')
    return RedirectResponse(next)
