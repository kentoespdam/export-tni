from sqlalchemy import Column, Integer, String
from src.core.db import Base


class SatkerModel(Base):
    __tablename__ = "satker"

    id = Column(Integer, primary_key=True)
    nama = Column(String)
