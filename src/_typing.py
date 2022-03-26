from typing import NewType, TypedDict

Argon2Hash = NewType("Argon2Hash", str)

class Config(TypedDict):
   port: int
   host: str
   reload: bool
   mongo_url: str