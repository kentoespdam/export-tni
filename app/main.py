from fastapi import FastAPI

from src.core.utility import Utility
from src.routers import main

app = FastAPI(
    title="Export Data TNI",
)

app.include_router(main.api_route)


@app.get("/")
async def root():
    return Utility.json_response(status=200, message="Root Path", error=[], data={})
