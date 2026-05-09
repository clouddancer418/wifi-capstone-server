import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "wifi_monitor.db"))

BUNDLED_DB_PATH = os.path.join(BASE_DIR, "wifi_monitor.db")

# Render의 영구 디스크 DB가 없으면, GitHub에 올라간 DB를 한 번 복사
if DB_PATH != BUNDLED_DB_PATH and not os.path.exists(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    shutil.copy(BUNDLED_DB_PATH, DB_PATH)

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