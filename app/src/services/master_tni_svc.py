from datetime import datetime
import io
import os
import math
from unittest import result
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pandas import DataFrame
from sqlalchemy.orm import Session

from ..models.cust_model import CustModel
from ..schema.master_tni import MasterTniSchema
from ..services.satker import get_satker_by_id
from ..models.master_tni_model import MasterTniModel
from pydantic import BaseModel
from ..core.utility import Utility
import pandas as pd
import numpy as np


class MasterTni(BaseModel):
    nosamw: str
    nama: str
    kotama: str
    satker: str


def get_master_tni(
    db_session: Session,
    db_coklit_session: Session,
    page: int,
    limit: int,
    sort: list[tuple[str, str]] | None,
    nosamw: str | None,
    nama: str | None,
    is_aktif: bool = True,
    satker_id: int = 0,
) -> JSONResponse:
    """
    Retrieve a list of MasterTniModel based on the provided parameters.

    Args:
        db_session (Session): The database session.
        db_coklit_session (Session): The coklit database session.
        page (int): Page number for pagination.
        limit (int): Number of items per page.
        sort (list[tuple[str, str]] | None): List of fields to sort by and their order.
        nosamw (str | None): Filter by nosamw.
        nama (str | None): Filter by nama.
        is_aktif (bool, optional): Flag to filter by active status. Defaults to True.
        satker_id (int, optional): ID of the satker. Defaults to 0.

    Returns:
        JSONResponse: A JSON response containing the retrieved data.
    """
    offset = max(0, page - 1) * limit
    satker = get_satker_by_id(satker_id, db_coklit_session)
    query = db_session.query(
        MasterTniModel.nosamw,
        MasterTniModel.nama,
        MasterTniModel.kotama,
        MasterTniModel.satker,
        MasterTniModel.is_aktif,
        CustModel.urjlw
    ).join(CustModel, MasterTniModel.nosamw == CustModel.nosamw).filter(MasterTniModel.is_aktif == is_aktif)

    if satker:
        query = query.filter(
            MasterTniModel.satker.like(f"%{satker.nama}%")
        )

    if nosamw:
        query = query.filter(
            MasterTniModel.nosamw == nosamw
        )

    if nama:
        query = query.filter(
            MasterTniModel.nama.like(f"%{nama}%")
        )

    total = query.count()

    if sort:
        for sort_field, sort_order in sort:
            field = getattr(MasterTniModel, sort_field)
            query = query.order_by(
                field.asc() if sort_order == "asc" else field.desc()
            )

    query = query.offset(offset).limit(limit)

    rows = query.all()
    result = []
    for row in rows:
        result.append({
            "nosamw": row.nosamw,
            "nama": row.nama,
            "kotama": row.kotama,
            "satker": row.satker,
            "is_aktif": row.is_aktif,
            "urjlw": row.urjlw,
        })
    total_pages = math.ceil(total / limit)

    return Utility.pagination(
        status=200 if result else 404,
        message="Data Found" if result else "Not Found",
        error=[],
        data=result,
        total=total,
        limit=limit,
        page=page,
        totalPages=total_pages,
        isFirst=page == 1,
        isLast=page == total_pages,
    )


def get_master_tni_by_nosamw(db: Session, nosamw: str) -> MasterTniModel | None:
    """Retrieve MasterTniModel by nosamw from the database.

    Args:
        db (Session): The database session.
        nosamw (str): The nosamw of the MasterTniModel to retrieve.

    Returns:
        MasterTniModel | None: The retrieved MasterTniModel or None if not found.
    """
    result = db.query(MasterTniModel).filter(
        MasterTniModel.nosamw == nosamw).first()
    return Utility.dict_response(
        status=200 if result else 404,
        message="Data Found" if result else "Not Found",
        error=[],
        data=result,
    )


def save_master_tni(db: Session, master_tni: MasterTniSchema) -> JSONResponse:
    """
    Save a new MasterTni to the database.

    Args:
        db (Session): The database session.
        master_tni (MasterTni): The MasterTni to be saved.

    Returns:
        JSONResponse: A JSON response indicating the result of the operation.
    """
    existing_master_tni = db.query(MasterTniModel).filter(
        MasterTniModel.nosamw == master_tni.nosamw).first()
    if existing_master_tni:
        return Utility.json_response(
            status=409, message="Master Tni already exists", error=[], data={}
        )
    try:
        new_data = MasterTniModel(
            nosamw=master_tni.nosamw,
            nama=master_tni.nama,
            kotama=master_tni.kotama,
            satker=master_tni.satker,
            is_aktif=master_tni.is_aktif
        )

        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return Utility.dict_response(
            status=201, message="Master Tni created", error=[], data=master_tni
        )
    except Exception as e:
        return Utility.dict_response(status=500, message="Server Error", error=e.args, data={})


def update_master_tni(
    db_session: Session,
    updated_master_tni: MasterTniSchema,
    nosamw: str
) -> JSONResponse:
    """Update a master tni by nosamw.

    Args:
    db_session (Session): The database session.
    updated_master_tni (MasterTni): The updated master tni.
    nosamw (str): The nosamw of the master tni to update.

    Returns:
    JSONResponse: A JSON response indicating the result of the operation.
    """
    existing_master_tni = db_session.query(
        MasterTniModel).filter_by(nosamw=nosamw).first()
    if not existing_master_tni:
        return Utility.json_response(
            status=404, message="Data Not Found", error=[], data={}
        )

    existing_master_tni.nama = updated_master_tni.nama
    existing_master_tni.kotama = updated_master_tni.kotama
    existing_master_tni.satker = updated_master_tni.satker
    existing_master_tni.is_aktif = updated_master_tni.is_aktif
    db_session.commit()
    db_session.refresh(existing_master_tni)

    return Utility.dict_response(status=200, message="Update Success", error=[], data=existing_master_tni)


def delete_master_tni(db_session: Session, nosamw: str) -> JSONResponse:
    """
    Delete a master tni by nosamw.

    Args:
    db_session (Session): The database session.
    nosamw (str): The nosamw of the master tni to delete.

    Returns:
    JSONResponse: A JSON response indicating the result of the deletion.
    """
    master_tni = db_session.query(MasterTniModel).filter(
        MasterTniModel.nosamw == nosamw).first()

    if not master_tni:
        return Utility.json_response(
            status=404, message="Data Not Found", error=[], data={})

    db_session.delete(master_tni)
    db_session.commit()

    return Utility.json_response(
        status=200, message="Delete Success", error=[], data={})


def remove_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(e)


def export_master_tni(
    db: Session,
    dbCoklit: Session,
    nosamw: str | None,
    nama: str | None,
    is_aktif: bool,
    satker_id: int | None,
    background_task: BackgroundTasks,
):
    try:
        query = db.query(
            MasterTniModel.nosamw,
            MasterTniModel.nama,
            MasterTniModel.kotama,
            MasterTniModel.satker,
            MasterTniModel.is_aktif,
            CustModel.urjlw
        ).join(
            CustModel,
            MasterTniModel.nosamw == CustModel.nosamw
        ).filter(MasterTniModel.is_aktif == is_aktif)

        if satker_id:
            satker = get_satker_by_id(satker_id, dbCoklit)
            likeNama = "%{}%".format(satker.nama)
            query = query.filter(MasterTniModel.satker.like(likeNama))

        if nosamw:
            query = query.filter(MasterTniModel.nosamw == nosamw)

        if nama:
            likeNama = "%{}%".format(nama)
            query = query.filter(MasterTniModel.nama.like(likeNama))

        data = []
        urut = 1
        for row in query.all():
            data.append(
                {
                    "urut": urut,
                    "nosamw": row.nosamw,
                    "nama": row.nama,
                    "kotama": row.kotama,
                    "satker": row.satker,
                    "is_aktif": row.is_aktif,
                    "urjlw": row.urjlw
                }
            )
            urut += 1

        df: DataFrame = pd.DataFrame(data)
        df.to_excel("master_tni.xlsx", index=False)
        file_response = FileResponse(
            "master_tni.xlsx", filename="master_tni.xlsx")
        background_task.add_task(remove_file, "master_tni.xlsx")
        return file_response
    except Exception as e:
        print(e)
        return Utility.json_response(
            status=e, message="Server Error", error=[], data={}
        )


def export_master_tni_csv(
    db: Session,
    dbCoklit: Session,
    nosamw: str | None,
    nama: str | None,
    is_aktif: bool,
    satker_id: int | None,
):
    try:
        query = db.query(
            MasterTniModel.nosamw,
            MasterTniModel.satker,
            CustModel.urjlw
        ).join(
            CustModel,
            MasterTniModel.nosamw == CustModel.nosamw
        ).filter(MasterTniModel.is_aktif == is_aktif)

        if satker_id:
            satker = get_satker_by_id(satker_id, dbCoklit)
            likeNama = "%{}%".format(satker.nama)
            query = query.filter(MasterTniModel.satker.like(likeNama))

        if nosamw:
            query = query.filter(MasterTniModel.nosamw == nosamw)

        if nama:
            likeNama = "%{}%".format(nama)
            query = query.filter(MasterTniModel.nama.like(likeNama))

        rows = query.all()

        data = pd.DataFrame(
            rows, columns=["No Sambungan", "Satker", "Golongan"])
        data["Golongan"] = data["Golongan"].astype(str)

        df = pd.DataFrame(data)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = (
            f"attachment; filename=master_tni_{
                datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        )
        return response
    except Exception as e:
        print(e)
        return Utility.json_response(
            status=e, message="Server Error", error=[], data={}
        )
