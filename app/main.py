from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routers import account_mappings as account_mappings_router
from app.api.routers import ui as ui_router

# Assuming app_router and auth_router are defined elsewhere or will be moved.
# For now, their original imports are removed as app/routes will be deleted.
# If they exist in app.api.routers, they should be added to the import above.
# Example: from app.api.routers import ui as ui_router, account_mappings, app_router, auth_router
from app.core.settings import settings

# from app.routes import ( # Old import from app/routes
#   app_router,
#   auth_router,
# )

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
# app.include_router(auth_router) # Re-enable if auth_router is available and imported
# app.include_router(app_router) # Re-enable if app_router is available and imported
app.include_router(account_mappings_router.router)
