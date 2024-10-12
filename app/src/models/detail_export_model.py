from sqlalchemy import Column, String, Integer, Double
from src.core.db import Base


class RekeningTniModel(Base):
    __tablename__ = "rekening_tni"

    id = Column(Integer, primary_key=True)
    pdam = Column(String)
    matra = Column(String)
    satker = Column(String)
    nosamw = Column(String)
    nama = Column(String)
    alamat = Column(String)
    periode = Column(String)
    met_l = Column(Double)
    met_l_ori = Column(Double)
    met_k = Column(Double)
    met_k_ori = Column(Double)
    pakai = Column(Double)
    pakai_ori = Column(Double)
    rata2 = Column(Double)
    rata2_ori = Column(Double)
    dnmet = Column(Double)
    r1 = Column(Double)
    r2 = Column(Double)
    r3 = Column(Double)
    r4 = Column(Double) 
    t1 = Column(Double)
    t2 = Column(Double)
    t3 = Column(Double)
    t4 = Column(Double)
    denda = Column(Double)
    ang_sb = Column(Double)
    jasa_sb = Column(Double)
