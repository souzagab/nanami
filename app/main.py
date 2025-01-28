from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config.settings import settings
from app.libs.pluggy.pluggy_client import PluggyAIClient
from app.libs.ynab.ynab_client import YNABClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for the FastAPI application.
    Handles initialization and cleanup of resources.
    """
    # Initialize clients
    app.state.ynab_client = YNABClient(
        access_token=settings.ynab_access_token,
        async_mode=settings.ynab_async_mode
    )
    app.state.pluggy_client = PluggyAIClient(
        client_id=settings.pluggy_client_id,
        client_secret=settings.pluggy_client_secret,
        async_mode=settings.pluggy_async_mode
    )

    try:
        yield
    finally:
        # Cleanup
        await app.state.ynab_client.aclose()
        await app.state.pluggy_client.async_close()


def create_application() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_application()
