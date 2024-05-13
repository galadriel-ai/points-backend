from typing import List

from fastapi import APIRouter

from points import api_logger
from points.routers.routes import admin_router
from points.routers.routes import auth_router
from points.routers.routes import dashboard_router

TAG_ROOT = "root"

router = APIRouter()
logger = api_logger.get()

routers_to_include: List[APIRouter] = [
    admin_router.router,
    auth_router.router,
    dashboard_router.router,
]
for router_to_include in routers_to_include:
    router.include_router(router_to_include)
