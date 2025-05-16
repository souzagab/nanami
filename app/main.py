from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routers import ui as ui_router
from app.core.settings import settings

APP_BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=settings.project_name)

# Mount static files
app.mount("/static", StaticFiles(directory=APP_BASE_DIR / "static"), name="static")

# Initialize templates - this instance can be used by routers
templates = Jinja2Templates(directory=APP_BASE_DIR / "templates")

# Store templates in app.state for easier access in routers
app.state.templates = templates

# Include UI router
app.include_router(ui_router.router)
