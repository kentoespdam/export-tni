from decimal import Decimal
from pydantic import BaseModel


class CustSchema(BaseModel):
    noreg:str
    nosamw: str
    nama: str
    alamat: str
    urjlw: str