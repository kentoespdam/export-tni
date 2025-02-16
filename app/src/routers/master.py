from typing import Annotated
from ..schema.master_tni import MasterTniSchema
from ..services.master_tni_svc import delete_master_tni, export_master_tni, export_master_tni_csv, get_master_tni, get_master_tni_by_nosamw, save_master_tni, update_master_tni
from ..core.utility import Utility
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session
from src.core.db import get_coklit_database_session, get_database_session

router = APIRouter(
    prefix="/api/master_tni",
    tags=["Master Data TNI"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root(
    page: int = Query(1, ge=1),
    limit: int = 10,
    sort: Annotated[list[str] | None, Query()] = None,
    nosamw: str | None = None,
    nama: str | None = None,
    is_aktif: bool = True,
    satker_id: str | None = None,
    db: Session = Depends(get_database_session),
    dbCoklit: Session = Depends(get_coklit_database_session),
):
    try:
        if satker_id is not None:
            satker_id = Utility.decodeId(satker_id)
        master_tni = get_master_tni(
            db, dbCoklit, page, limit, sort, nosamw, nama, is_aktif, satker_id)
        return master_tni
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.get("/{nosamw}")
async def detail(nosamw: int, db: Session = Depends(get_database_session)):
    try:
        return get_master_tni_by_nosamw(db, nosamw)
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.post("/")
async def create(request: MasterTniSchema, db: Session = Depends(get_database_session)):
    try:
        return save_master_tni(db, request)
    except Exception as e:
        print(e)
        return Utility.dict_response(status=e, message="Server Error", error=[], data={})


@router.put("/{nosamw}")
async def update(nosamw: int, request: MasterTniSchema, db: Session = Depends(get_database_session)):
    try:
        return update_master_tni(db, request, nosamw)
    except Exception as e:
        print(e)
        return Utility.dict_response(status=e, message="Server Error", error=[], data={})


@router.delete("/{nosamw}")
async def delete(nosamw: int, db: Session = Depends(get_database_session)):
    try:
        return delete_master_tni(db, nosamw)
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.get("/export/excel")
async def export(
    nosamw: str | None = None,
    nama: str | None = None,
    is_aktif: bool = True,
    satker_id: str | None = None,
    db: Session = Depends(get_database_session),
    dbCoklit: Session = Depends(get_coklit_database_session),
    background_task: BackgroundTasks = None,
):
    try:
        if satker_id is not None:
            satker_id = Utility.decodeId(satker_id)
        master_tni = export_master_tni(
            db, dbCoklit, nosamw, nama, is_aktif, satker_id, background_task)
        return master_tni
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})


@router.get("/export/csv")
async def export(
    nosamw: str | None = None,
    nama: str | None = None,
    is_aktif: bool = True,
    satker_id: str | None = None,
    db: Session = Depends(get_database_session),
    dbCoklit: Session = Depends(get_coklit_database_session),
):
    try:
        if satker_id is not None:
            satker_id = Utility.decodeId(satker_id)
        master_tni = export_master_tni_csv(
            db, dbCoklit, nosamw, nama, is_aktif, satker_id)
        return master_tni
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})
