from contextlib import asynccontextmanager

from fastapi import FastAPI
from libs.pluggy.pluggy_client import PluggyAIClient
from libs.ynab.ynab_client import YNABClient

from config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ynab_client = YNABClient()
    app.state.pluggy_client = PluggyAIClient()

    try:
        yield
    finally:
        await app.state.ynab_client.aclose()
        await app.state.pluggy_client.close()


app = FastAPI(lifespan=lifespan, debug=Settings.debug)

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "I'm alive!"}
