import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute, iter_route_contexts
from starlette.applications import Starlette
from starlette.routing import Mount

from config import (
    ALLOWED_ORIGINS,
    DASHBOARD_PATH,
    DOCS,
    HTTP_WEBROOT_PATH,
    XRAY_SUBSCRIPTION_PATH,
)

__version__ = "0.8.4"


@asynccontextmanager
async def lifespan(app: FastAPI):
    dashboard.startup()

    from app.jobs import start_core, stop_core
    from app.jobs.send_notifications import shutdown_notifications
    from app.telegram import start_bot

    start_core()
    start_bot()

    scheduler.start()

    try:
        yield
    finally:
        shutdown_notifications()
        stop_core()
        scheduler.shutdown()


app = FastAPI(
    title="MarzbanAPI",
    description="Unified GUI Censorship Resistant Solution Powered by Xray",
    version=__version__,
    docs_url="/docs" if DOCS else None,
    redoc_url="/redoc" if DOCS else None,
    lifespan=lifespan,
)


subscription_app = FastAPI(
    title="MarzbanSubscriptions",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


scheduler = BackgroundScheduler(
    {"apscheduler.job_defaults.max_instances": 20},
    timezone="UTC",
)


logger = logging.getLogger("uvicorn.error")


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app import dashboard, jobs, routers, telegram  # noqa
from app.routers import subscription


subscription_app.include_router(subscription.router)


dashboard_at_root = (
    bool(HTTP_WEBROOT_PATH)
    or DASHBOARD_PATH.rstrip("/") == ""
)

routers.include_routers(
    app,
    include_home=not dashboard_at_root,
)

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)


paths = [
    f"{r.path}/"
    for r in iter_route_contexts(app.routes)
]

paths.append("/api/")


if f"/{XRAY_SUBSCRIPTION_PATH}/" in paths:
    raise ValueError(
        f"you can't use /{XRAY_SUBSCRIPTION_PATH}/ "
        f"as subscription path it reserved for {app.title}"
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    details = {}

    for error in exc.errors():
        details[error["loc"][-1]] = error.get("msg")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": details}),
    )


subscription_path = f"/{XRAY_SUBSCRIPTION_PATH.strip('/')}"

if HTTP_WEBROOT_PATH == "":
    marzban_path = ""
else:
    marzban_path = HTTP_WEBROOT_PATH.rstrip("/") or "/"

application = Starlette(
    lifespan=lifespan,
    routes=[
        Mount(
            subscription_path,
            app=subscription_app,
            name="subscription",
        ),
        Mount(
            marzban_path,
            app=app,
            name="marzban",
        ),
    ],
)
