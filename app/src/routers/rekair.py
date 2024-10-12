from fastapi import APIRouter
from src.core.contant import SUCCESS
from ..core.utility import Utility
from ..services.rekair import getRekair

router = APIRouter(
    prefix="/api/rekair",
    tags=["Rekair"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{periode}")
async def root(periode: str):
    try:
        data = await getRekair(periode)
        return Utility.dict_response(
            status=SUCCESS,
            message="Success",
            error=[],
            data=data
        )
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})
