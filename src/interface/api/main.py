from fastapi import FastAPI
from src.interface.api.routes.router_common import common_router
from src.interface.api.routes.router_context import context_router

app = FastAPI()
app.include_router(common_router)
app.include_router(context_router)