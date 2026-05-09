import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# GitHub에 올라간 기본 DB
SOURCE_DB = os.path.join(BASE_DIR, "wifi_monitor.db")

# Render 영구 디스크 DB
DB_PATH = os.getenv("DB_PATH", SOURCE_DB)

# Render 디스크 DB가 없거나 비어있으면 기본 DB 복사
if DB_PATH != SOURCE_DB:
    need_copy = (
        not os.path.exists(DB_PATH)
        or os.path.getsize(DB_PATH) < 10000
    )

    if need_copy:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        shutil.copy(SOURCE_DB, DB_PATH)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()