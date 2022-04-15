from fastapi import Response, APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from ..gql import handle_login
from ..models import JsonResponse

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
    response_description = "Redirected to the next resource.",
)
async def logout(response: Response, next: str = '/'):
    response.delete_cookie('auth')
    return RedirectResponse(next)

@router.post(
    '/login',
    response_class = JSONResponse,
    response_model = JsonResponse,
    summary = "Log in to an account.",
    responses = {
        200: {
            "description": "Logged in to the specified account.",
            "model": UserPasswordInput
        },
        400: {
            "description": "Invalid username or password.",
        }
    }
)
async def login(
    response: Response,
    data: UserPasswordInput,
):
    token_dict = handle_login(response, data.username, data.password)

    if not token_dict:
        raise HTTPException(status_code = 400, detail = "Invalid username or password.")