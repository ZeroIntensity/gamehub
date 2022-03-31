from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .schema import schema
from fastapi.staticfiles import StaticFiles
import os
import importlib
from .gql import get_context

app = FastAPI()
app.include_router(GraphQLRouter(schema, context_getter = get_context), prefix = "/graphql")
app.mount("/static", StaticFiles(directory = "./static"), name = "static")

for root, dirs, files in os.walk('./src/routers'):
    for file in files:
        if file.endswith('.py'):
            lib = importlib.import_module(f'src.routers.{file[:-3]}')
            app.include_router(lib.router, prefix = lib.prefix)
