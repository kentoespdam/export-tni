import os
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from numpy import number
from pandas import DataFrame
from sqlalchemy.orm import Session
from ..services.satker import get_satker_by_id
from ..models.master_tni_model import MasterTniModel
from pydantic import BaseModel
from ..core.utility import Utility
import pandas as pd


class MasterTni(BaseModel):
    nosamw: str
    nama: str
    kotama: str
    satker: str


def get_master_tni(
        db: Session,
        dbCoklit: Session,
        offset: int,
        limit: int,
        sort: list[list[str]] | None,
        nosamw: str | None,
        nama: str | None,
        is_aktif: bool = True,
        satker_id: int = 0
):
    satker = get_satker_by_id(satker_id, dbCoklit)
    query = db.query(MasterTniModel).filter(
        MasterTniModel.is_aktif == is_aktif)
    if satker:
        likeNama = "%{}%".format(satker.nama)
        query = query.filter(MasterTniModel.satker.like(likeNama))
    if nosamw:
        query = query.filter(MasterTniModel.nosamw == nosamw)

    if nama:
        likeNama = "%{}%".format(nama)
        query = query.filter(MasterTniModel.nama.like(likeNama))
    total = query.count()
    if sort is not None and len(sort) > 0:
        for s in sort:
            slist = list(s.split(","))
            field = getattr(MasterTniModel, slist[0])
            order = slist[1] if len(slist) > 1 else "asc"
            query = query.order_by(
                field.asc() if order == "asc" else field.desc())
    else:
        query = query.order_by(MasterTniModel.nosamw.asc())
    # print(query)
    result = query.offset(offset).limit(limit).all()

    return Utility.pagination(
        status=200 if result else 404,
        message="Data Found" if result else "Not Found",
        error=[],
        data=result,
        total=total,
        limit=limit,
        offset=offset
    )


def get_master_tni_by_nosamw(db: Session, nosamw: str) -> MasterTniModel | None:
    result = db.query(MasterTniModel).filter(
        MasterTniModel.nosamw == nosamw).first()
    return Utility.dict_response(
        status=200 if result else 404,
        message="Data Found" if result else "Not Found",
        error=[],
        data=result
    )


def save_master_tni(db: Session, master_tni: MasterTni):
    # check data is exist
    result = get_master_tni_by_nosamw(db, master_tni.nosamw)
    if result:
        return Utility.json_response(
            status=409,
            message="Data Already Exist",
            error=[],
            data={}
        )

    db.add(master_tni)
    db.commit()
    db.refresh(master_tni)
    return master_tni


def update_master_tni(db: Session, master_tni: MasterTni, nosamw: str):
    # check data is exist
    rekening = db.query(MasterTniModel).filter(
        MasterTniModel.nosamw == nosamw).first()
    if not rekening:
        return Utility.json_response(
            status=404,
            message="Data Not Found",
            error=[],
            data={}
        )

    rekening.nama = master_tni.nama
    rekening.kotama = master_tni.kotama
    rekening.satker = master_tni.satker
    rekening.is_aktif = master_tni.is_aktif
    db.commit()
    db.refresh(rekening)

    return master_tni


def delete_master_tni(db: Session, nosamw: str):
    # check data is exist
    rekening = db.query(MasterTniModel).filter(
        MasterTniModel.nosamw == nosamw).first()
    if not rekening:
        return Utility.json_response(
            status=404,
            message="Data Not Found",
            error=[],
            data={}
        )

    db.delete(rekening)
    db.commit()
    return rekening


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
        background_task: BackgroundTasks
):
    try:
        satker = get_satker_by_id(satker_id, dbCoklit)
        query = db.query(MasterTniModel).filter(
            MasterTniModel.is_aktif == is_aktif)
        
        if satker:
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
            data.append({
                "urut": urut,
                "nosamw": row.nosamw,
                "nama": row.nama,
                "kotama": row.kotama,
                "satker": row.satker,
                "is_aktif": row.is_aktif
            })
            urut += 1

        df: DataFrame = pd.DataFrame(data)
        df.to_excel('master_tni.xlsx', index=False)
        file_response = FileResponse(
            'master_tni.xlsx', filename='master_tni.xlsx')
        background_task.add_task(remove_file, 'master_tni.xlsx')
        return file_response
    except Exception as e:
        print(e)
        return Utility.json_response(status=e, message="Server Error", error=[], data={})
