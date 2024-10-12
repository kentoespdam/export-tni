from typing import Generator

import pymysql
from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

billingEngine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))
coklitEngine = create_engine(str(settings.COKLIT_DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=billingEngine)
SessionCoklit = sessionmaker(autocommit=False, autoflush=False, bind=coklitEngine)

Base = declarative_base()


def get_database_session() -> Generator:
    try:
        # print(settings.get_mysql_dsn())
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_coklit_database_session() -> Generator:
    try:
        db = SessionCoklit()
        yield db
    finally:
        db.close()

def get_raw_database_session():
    return pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        database=settings.DB_NAME,
        port=settings.DB_PORT,
        # cursorclass=pymysql.cursors.DictCursor
    )