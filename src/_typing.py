from typing import NewType, Literal, TypedDict

class Comment(TypedDict):
    author: str
    likes: int
    content: str

Argon2Hash = NewType("Argon2Hash", str)
AccountType = Literal["user", "admin", "owner", "developer"]
