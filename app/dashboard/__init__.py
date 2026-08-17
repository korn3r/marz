import atexit
import os
import subprocess
from pathlib import Path

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import app
from config import DEBUG, DASHBOARD_PATH, HTTP_WEBROOT_PATH, UVICORN_PORT


base_dir = Path(__file__).parent
build_dir = base_dir / "build"
statics_dir = build_dir / "statics"


dashboard_at_root = (
    bool(HTTP_WEBROOT_PATH)
    or DASHBOARD_PATH.rstrip("/") == ""
)


def get_dashboard_html() -> str:
    html_path = build_dir / "index.html"

    if not html_path.is_file():
        raise FileNotFoundError(
            f"Dashboard index not found: {html_path}"
        )

    html = html_path.read_text(encoding="utf-8")

    if HTTP_WEBROOT_PATH and HTTP_WEBROOT_PATH != "/":
        html = html.replace(
            '="/statics/',
            f'="{HTTP_WEBROOT_PATH.rstrip("/")}/statics/',
        )

    return html


def dashboard_index() -> HTMLResponse:
    return HTMLResponse(
        content=get_dashboard_html(),
        status_code=200,
    )


def build():
    proc = subprocess.Popen(
        [
            "npm",
            "run",
            "build",
            "--",
            "--outDir",
            build_dir,
            "--assetsDir",
            "statics",
        ],
        cwd=base_dir,
    )
    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError(
            f"Dashboard build failed with exit code {proc.returncode}"
        )


def run_dev():
    proc = subprocess.Popen(
        [
            "npm",
            "run",
            "dev",
            "--",
            "--host",
            "0.0.0.0",
            "--clearScreen",
            "false",
            "--base",
            os.path.join(DASHBOARD_PATH, ""),
        ],
        env={
            **os.environ,
            "UVICORN_PORT": str(UVICORN_PORT),
        },
        cwd=base_dir,
    )

    atexit.register(proc.terminate)


def register_routes():
    app.mount(
        "/statics/",
        StaticFiles(
            directory=statics_dir,
            html=False,
        ),
        name="statics",
    )

    if dashboard_at_root:
        app.add_api_route(
            "/",
            dashboard_index,
            methods=["GET"],
            response_class=HTMLResponse,
            include_in_schema=False,
            name="dashboard",
        )
    else:
        app.add_api_route(
            DASHBOARD_PATH.rstrip("/") + "/",
            dashboard_index,
            methods=["GET"],
            response_class=HTMLResponse,
            include_in_schema=False,
            name="dashboard",
        )


def startup():
    if DEBUG:
        run_dev()
    else:
        if not build_dir.is_dir():
            build()


register_routes()
