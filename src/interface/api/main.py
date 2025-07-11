from fastapi import FastAPI
from src.interface.api.routes.router_common import common_router
from src.interface.api.routes.router_context import context_router
from src.interface.api.routes.router_text import text_router

app = FastAPI()
app.include_router(common_router, tags=["Common"])
app.include_router(context_router, tags=["Context"])
app.include_router(text_router, tags=["Text"])