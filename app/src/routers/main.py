from fastapi import APIRouter

from . import export, master, rekair, satker
api_route = APIRouter()

api_route.include_router(master.router)
api_route.include_router(export.router)
api_route.include_router(rekair.router)
api_route.include_router(satker.router)
