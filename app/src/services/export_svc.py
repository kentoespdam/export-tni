import io
import math
from typing import Any, Dict

from fastapi.responses import StreamingResponse
from src.models.satker import SatkerModel
from src.models.detail_export_model import RekeningTniModel
from src.models.sync_log_model import SyncLogModel
from sqlalchemy.orm import Session
import pandas as pd
from src.schema.rekening_tni import RekeningTniUpdateRequest
from src.services.rekair import get_rekening_tni
from src.core.db import coklitEngine
from src.core.utility import Utility


def get_tagihan(
    db: Session,
    periode: str,
    page: int,
    limit: int,
    sort: list[list[str]] | None = None,
    nosamw: str | None = None,
    nama: str | None = None,
) -> Dict[str, any]:
    """
    Retrieve tagihan data from the database.

    Args:
    db (Session): Database session.
    periode (str): Periode.
    offset (int): Offset.
    limit (int): Limit.
    sort (list[list[str]] | None): Sort query.
    nosamw (str | None): Filter by nosamw.
    nama (str | None): Filter by nama.

    Returns:
    Dict[str, any]: A dictionary containing the response data.
    """
    offset = max(0, page - 1) * limit
    stmt = db.query(RekeningTniModel)
    stmt = stmt.filter(RekeningTniModel.periode == periode)
    if nosamw:
        stmt = stmt.filter(RekeningTniModel.nosamw == nosamw)
    if nama:
        stmt = stmt.filter(RekeningTniModel.nama.like(f"%{nama}%"))

    total = stmt.count()
    if sort:
        for s in sort:
            slist = s.split(",")
            field = getattr(RekeningTniModel, slist[0])
            order = slist[1] if len(slist) > 1 else "asc"
            stmt = stmt.order_by(field.asc() if order == "asc" else field.desc())

    result: list[RekeningTniModel] = stmt.offset(offset).limit(limit).all()
    totalPages = math.ceil(total / limit)

    for r in result:
        r.id = Utility.encodeId(r.id)

    return Utility.pagination(
        status=200 if result else 404,
        message="Data Found" if result else "Not Found",
        error=[],
        data=result,
        total=total,
        limit=limit,
        page=page,
        totalPages=totalPages,
        isFirst=page == 1,
        isLast=page == totalPages,
    )


def getTagihanById(id: int, db: Session) -> Dict[str, Any]:
    """
    Retrieve a tagihan by ID from the database.

    Args:
        id (int): Tagihan ID.
        db (Session): Database session.

    Returns:
        Dict[str, Any]: A dictionary containing the response data.
    """
    query = db.query(RekeningTniModel).filter(RekeningTniModel.id == id)
    result: RekeningTniModel | None = query.first()
    if result:
        result.id = Utility.encodeId(result.id)
    return Utility.dict_response(
        status=200 if result else 404,
        message="Data Found" if result else "Not Found",
        error=[],
        data=result if result else {},
    )


def get_latest_sync(periode: str, db: Session) -> bool:
    """
    Check if a sync log exists for the given periode.

    Args:
        periode (str): Periode to check.
        db (Session): Database session.

    Returns:
        bool: Whether a sync log exists for the given periode.
    """
    query = db.query(SyncLogModel).filter(SyncLogModel.periode == periode).exists()
    exists = db.query(query).scalar()
    return exists


def save_sync(periode: str, db: Session) -> None:
    """
    Save a sync log to the database.

    Args:
        periode (str): The periode to save.
        db (Session): The database session.

    Returns:
        None
    """
    db.add(SyncLogModel(periode=periode))
    db.commit()


def tarik_data(periode: str, db: Session) -> Dict[str, Any]:
    """
    Retrieve data from the database and save it to the coklit database.

    Args:
        periode (str): The periode to retrieve.
        db (Session): The database session.

    Returns:
        Dict[str, Any]: A dictionary containing the response data.
    """
    isSynced = get_latest_sync(periode, db)
    if isSynced:
        return Utility.dict_response(
            status=403, message="Already Synced", error=[], data={}
        )

    data: pd.DataFrame = get_rekening_tni(periode)
    if data is None:
        return Utility.dict_response(status=404, message="Not Found", error=[], data={})

    data.to_sql(
        con=coklitEngine,
        name="rekening_tni",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )
    save_sync(periode, db)

    return Utility.dict_response(
        status=201,
        message="Success Synced",
        error=[],
        data={"periode": periode, "total": len(data)},
    )


def update_tagihan(
    id: int, data: RekeningTniUpdateRequest, db: Session, db_billing: Session
) -> Dict[str, Any]:
    """
    Update a tagihan by ID from the database.

    Args:
        id (int): Tagihan ID.
        data (RekeningTniUpdateRequest): The data to update.
        db (Session): Database session.
        db_billing (Session): Billing database session.

    Returns:
        Utility.Response: A dictionary containing the response data.
    """
    tagihan = db.get(RekeningTniModel, id)
    if tagihan is None:
        return Utility.dict_response(
            status=404, message="Tagihan not found", error=[], data={}
        )

    # rekening = detail_rekening(tagihan.nosamw, tagihan.periode, db_billing)
    beban1 = float(min(10, float(data.pakai)))
    beban2 = float(min(10, max(0, float(data.pakai) - beban1)))
    beban3 = float(max(0, float(data.pakai) - beban1 - beban2))

    tagihan.met_l = data.met_l
    tagihan.met_k = data.met_k
    tagihan.pakai = data.pakai
    tagihan.rata2 = data.rata2
    tagihan.r1 = beban1 * tagihan.t1
    tagihan.r2 = beban2 * tagihan.t2
    tagihan.r3 = beban3 * tagihan.t3

    db.commit()
    return Utility.json_response(
        status=201, message="Tagihan updated", error=[], data={}
    )


def export_csv(periode: str, satker_id: int, db: Session) -> StreamingResponse:
    """Export Rekening TNI to CSV.

    Args:
        periode (str): Periode.
        satker_id (int): Satker ID.
        db (Session): Database session.

    Returns:
        StreamingResponse: A StreamingResponse with the CSV data.
    """
    satker = db.query(SatkerModel).filter(SatkerModel.id == satker_id).first()
    stmt = db.query(RekeningTniModel).filter(RekeningTniModel.periode == periode)
    stmt = stmt.filter(RekeningTniModel.satker == satker.nama)
    rows = stmt.all()
    if rows is None:
        return Utility.dict_response(status=404, message="Not Found", error=[], data={})

    data = []
    for row in rows:
        data.append(
            {
                "PDAM": row.pdam,
                "Matra/Kesatuan": row.matra,
                "Nama Satker": row.satker,
                "Nomor Sambungan": row.nosamw,
                "Nama": row.nama,
                "Alamat": row.alamat,
                "Periode": row.periode,
                "Stan lalu": int(row.met_l),
                "Stan kini": int(row.met_k),
                "Stan Angkat": int(0),
                "Pakai (m3)": int(row.pakai),
                "Tariff": int(0),
                "Tagihan": int(row.r1 + row.r2 + row.r3 + row.r4),
                "Denda": int(row.denda),
                "Total Tagihan": int(
                    row.dnmet
                    + row.r1
                    + row.r2
                    + row.r3
                    + row.r4
                    + row.denda
                    + row.ang_sb
                    + row.jasa_sb
                ),
                "Pemeliharaan": int(0),
                "Administrasi": int(row.dnmet),
                "Kelainan": "",
            }
        )
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = (
        f"attachment; filename=rekening_tni_{satker.nama}_{periode}.csv"
    )
    return response
