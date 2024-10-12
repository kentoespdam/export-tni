from pydantic import BaseModel


class SatkerSchema(BaseModel):
    id: int
    nama: str