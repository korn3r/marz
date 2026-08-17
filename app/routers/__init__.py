from fastapi import APIRouter

from . import (
    admin,
    core,
    home,
    node,
    system,
    user,
    user_template,
)


api_router = APIRouter(prefix="/api")

api_routers = [
    admin.router,
    core.router,
    node.router,
    system.router,
    user_template.router,
    user.router,
]

for router in api_routers:
    api_router.include_router(router)


def include_routers(app, include_home: bool = True):
    app.include_router(api_router)

    if include_home:
        app.include_router(home.router)


__all__ = ["api_router", "include_routers"]
