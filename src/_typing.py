from typing import NewType, TypedDict

Argon2Hash = NewType("Argon2Hash", str)

class AppConfig(TypedDict):
    ip: str
    port: int
    extra: dict
    mongo_url: str

class Config(TypedDict):
    production: bool
    prod: AppConfig
    dev: AppConfig