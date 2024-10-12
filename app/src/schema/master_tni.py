from pydantic import BaseModel


class MasterTniSchema(BaseModel):
    nosamw: str
    nama: str
    kotama: str
    satker: str
    is_aktif: bool