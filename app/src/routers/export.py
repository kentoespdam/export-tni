from typing import Annotated

from src.schema.rekening_tni import RekeningTniUpdateRequest
from ..services.export_svc import export_csv, get_tagihan, getTagihanById, tarik_data, update_tagihan
from ..core.utility import Utility
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..core.db import get_coklit_database_session, get_database_session

router = APIRouter(
    prefix="/api/tni",
    tags=["Export Data TNI"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{periode}")
def index(
    periode: str,
    page: int = Query(1, ge=1),
    limit: int = 10,
    sort: Annotated[list[str] | None, Query()] = None,
    nosamw: str | None = None,
    nama: str | None = None,
    db: Session = Depends(get_coklit_database_session)
):
    try:
        data = get_tagihan(db, periode, page, limit, sort, nosamw, nama)
        return data
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.get("/{id}/detail")
def index(id: str, db: Session = Depends(get_coklit_database_session)):
    try:
        id = Utility.decodeId(id)
        data = getTagihanById(id, db)
        return data
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.get("/{periode}/{satker_id}/csv")
async def get_csv(periode: str, satker_id: str, db: Session = Depends(get_coklit_database_session)):
    satker_id = Utility.decodeId(satker_id)
    try:
        data = export_csv(periode, satker_id, db)
        return data
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.get("/{periode}/tarik_data")
async def sync(
    periode: str,
    coklitSession: Session = Depends(get_coklit_database_session)
):
    try:
        data = tarik_data(periode, coklitSession)
        return data
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.put("/{id}")
async def update(
    id: str,
    request: RekeningTniUpdateRequest,
    db: Session = Depends(get_coklit_database_session),
    db1: Session = Depends(get_database_session)
):
    try:
        id = Utility.decodeId(id)
        return update_tagihan(id, request, db, db1)
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})
