from decimal import Decimal
from pydantic import BaseModel

from src.schema.rekair_schm import RekairSchema


class SyncLog(BaseModel):
    periode: str
    created_at: str


class RekeningTni(RekairSchema):
    pdam: str
    matra: str
    satker: str
    met_l_ori: Decimal
    met_k_ori: Decimal
    pakai_ori: Decimal
    rata2_ori: Decimal
    isAktif: bool


class RekeningTniUpdateRequest(BaseModel):
    nosamw: str
    met_l: Decimal
    met_k: Decimal
    pakai: Decimal

ExportColumns = [
    "pdam",
    "matra",
    "satker",
    "nosamw",
    "nama",
    "alamat",
    "periode",
    "met_l",
    "met_l_ori",
    "met_k",
    "met_k_ori",
    "pakai",
    "pakai_ori",
    "rata2",
    "rata2_ori",
    "dnmet",
    "r1",
    "r2",
    "r3",
    "r4",
    "denda",
    "ang_sb",
    "jasa_sb"
]
