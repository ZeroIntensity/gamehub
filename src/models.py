from pydantic import BaseModel

class JsonResponse(BaseModel):
    message: str
    status: int