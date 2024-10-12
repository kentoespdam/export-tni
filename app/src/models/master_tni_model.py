from sqlalchemy import Boolean, Column, String

from src.core.db import Base


class MasterTniModel(Base):
    __tablename__ = "master_tni"
    nosamw = Column(String, primary_key=True)
    nama = Column(String)
    kotama = Column(String)
    satker = Column(String)
    is_aktif = Column(Boolean)
