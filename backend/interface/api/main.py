from fastapi import FastAPI

from backend.interface.api.routes.router_context import context_router
from backend.interface.api.routes.router_deletes import deletes_router
from backend.interface.api.routes.router_develop import develop_router
from backend.interface.api.routes.router_service import service_router
from backend.interface.api.routes.router_text import text_router
from backend.interface.api.routes.router_common import common_router
from backend.interface.api.routes.router_statistics import statistics_router
from backend.logger import setup_logging
from backend.config import LoggingConfig

app = FastAPI()
setup_logging(LoggingConfig())

# TODO: add sorter for endpoints
app.include_router(common_router, tags=["Common"])
app.include_router(develop_router, tags=["Develop"])
app.include_router(context_router, tags=["Context"])
app.include_router(text_router, tags=["Text"])
app.include_router(service_router, tags=["Service"])
app.include_router(deletes_router, tags=["Deletes"])
app.include_router(statistics_router, prefix="/api", tags=["Statistics"])
