from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import Settings
from app.libs.pluggy.pluggy_client import PluggyAIClient
from app.libs.ynab.ynab_client import YNABClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ynab_client = YNABClient()
    app.state.pluggy_client = PluggyAIClient()

    try:
        yield
    finally:
        await app.state.ynab_client.aclose()
        await app.state.pluggy_client.async_close()


app = FastAPI(lifespan=lifespan, debug=Settings.debug)

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "I'm alive!"}
