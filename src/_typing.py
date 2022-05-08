from typing import NewType, Literal, TypedDict, List

PostID = NewType("PostID", str)

class Comment(TypedDict):
    author: str
    likes: List[str]
    content: str
    epoch: float
    id: PostID

class ProfileComment(TypedDict):
    game: str 
    epoch: float
    content: str
    id: str

RoomMessageType = Literal["message", "notification"]

class RoomMessage(TypedDict):
    type: RoomMessageType
    message: str
    author: str

Argon2Hash = NewType("Argon2Hash", str)
AccountType = Literal["user", "admin", "owner", "developer"]