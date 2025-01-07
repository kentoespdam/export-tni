from sqlalchemy import Column, String, Double
from src.core.db import Base


class CustModel(Base):
    __tablename__ = "cust"
    noreg = Column(String, primary_key=True)
    nosamw = Column(String)
    nama = Column(String)
    alamat = Column(String)
    urjlw = Column(String)
