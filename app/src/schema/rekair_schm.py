from decimal import Decimal
from pydantic import BaseModel


class RekairSchema(BaseModel):
    nosamw: str
    alamat: str
    periode: str
    met_l: str
    met_k: str
    pakai: Decimal
    rata2: Decimal
    dnmet: Decimal
    r1: Decimal
    r2: Decimal
    r3: Decimal
    r4: Decimal
    t1: Decimal
    t2: Decimal
    t3: Decimal
    t4: Decimal
    denda: Decimal
    ang_sb: Decimal
    jasa_sb: Decimal
    stattrek: str
