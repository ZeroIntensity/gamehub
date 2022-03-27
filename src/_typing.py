from typing import NewType, Literal

Argon2Hash = NewType("Argon2Hash", str)
AccountType = Literal["user", "admin", "owner", "developer"]
