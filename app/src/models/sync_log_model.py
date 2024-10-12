from sqlalchemy import Column, String
from ..core.db import Base

class SyncLogModel(Base):
    __tablename__ = "sync_log"
    periode = Column(String, primary_key=True)
    # created_at = Column(TIMESTAMP)
