from contextlib import asynccontextmanager

from fastapi import FastAPI
from libs.ynab.ynab_client import YNABClient

from config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ynab_client = YNABClient(
        access_token=Settings.ynab_access_token,
        async_mode=Settings.ynab_async_mode
    )
    try:
        yield
    finally:
        await app.state.ynab_client.aclose()

app = FastAPI(lifespan=lifespan, debug=Settings.debug)

@app.get("/healthcheck")
async def healthcheck():
  return {"message": "I'm alive!"}
