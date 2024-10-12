from sqlalchemy import Column, String, Double
from src.core.db import Base


class RekairModel(Base):
    __tablename__ = "rekair"
    nosamw=Column(String, primary_key=True)
    alamat=Column(String)
    periode=Column(String)
    met_l=Column(Double)
    met_k=Column(Double)
    pakai=Column(Double)
    rata2=Column(Double)
    dnmet=Column(Double)
    r1=Column(Double)
    r2=Column(Double)
    r3=Column(Double)
    r4=Column(Double)
    t1=Column(Double)
    t2=Column(Double)
    t3=Column(Double)
    t4=Column(Double)
    denda=Column(Double)
    ang_sb=Column(Double)
    jasa_sb=Column(Double)
    statrek=Column(String)