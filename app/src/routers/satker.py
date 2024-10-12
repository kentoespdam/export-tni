from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.satker import get_satker
from src.core.db import get_coklit_database_session
from src.core.utility import Utility

router = APIRouter(
    prefix="/api/satker",
    tags=["Satker"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root(db: Session = Depends(get_coklit_database_session)):
    try:
        return get_satker(db)
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})
