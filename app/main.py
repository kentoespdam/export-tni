from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.utility import Utility
from src.routers import main

app = FastAPI(
    title="Export Data TNI",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main.api_route)


@app.get("/")
async def root():
    return Utility.json_response(status=200, message="Root Path", error=[], data={})
