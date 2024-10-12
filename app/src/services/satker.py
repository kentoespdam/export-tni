from typing import Dict
from sqlalchemy.orm import Session

from ..schema.satker import SatkerSchema
from ..core.utility import Utility
from ..models.satker import SatkerModel


def get_satker(db: Session) -> Dict[str, any]:
    rows = db.query(SatkerModel).all()
    for row in rows:
        row.id = Utility.encodeId(row.id)
    return Utility.dict_response(
        status=200 if rows else 404,
        message="Data Found" if rows else "Not Found",
        error=[],
        data=rows if rows else {},
    )


def get_satker_by_id(id: int, db: Session) -> SatkerSchema | None:
    return db.query(SatkerModel).filter(SatkerModel.id == id).first()
