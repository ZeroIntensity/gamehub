import os
from typing import Optional
import jwt
import time
from ..config import config

__all__ = (
    "sign_jwt",
    "decode_jwt"
)

SECRET: str = os.environ['JWT_SECRET']
ALGORITHM: str = os.environ['JWT_ALGORITHM']

def sign_jwt(uid: str):
    payload = {
        "user_id": uid,
        "expires": time.time() + config.auth_validation_time
    }

    return jwt.encode(payload, SECRET, algorithm = ALGORITHM)

def decode_jwt(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms = [ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return {}