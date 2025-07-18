from fastapi import FastAPI
from src.interface.api.routes.router_develop import develop_router
from src.interface.api.routes.router_context import context_router
from src.interface.api.routes.router_text import text_router
from src.interface.api.routes.router_service import service_router
from src.interface.api.routes.router_deletes import deletes_router

app = FastAPI()

#TODO: add sorter for endpoints
app.include_router(develop_router, tags=["Develop"])
app.include_router(context_router, tags=["Context"])
app.include_router(text_router, tags=["Text"])
app.include_router(service_router, tags=["Service"])
app.include_router(deletes_router, tags=["Deletes"])