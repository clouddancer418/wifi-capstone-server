from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    # 기본 정보
    id = Column(Integer, primary_key=True, index=True)

    # WiFi 정보
    ssid = Column(String, nullable=True)
    bssid = Column(String, nullable=True)
    rssi = Column(Integer, nullable=True)
    latency = Column(Float, nullable=True)

    # 위치 정보
    building = Column(String, nullable=False)   # 공학관 / 학생회관 / 도서관
    floor = Column(Integer, nullable=False)     # 층 (숫자)
    location_name = Column(String, nullable=True)  # 선택 (예: "공학관 4층 복도")

    # 네트워크 추가 정보
    download_speed = Column(Float, nullable=True)
    link_speed = Column(Integer, nullable=True)

    # 분석 결과
    score = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # 좋음 / 보통 / 나쁨

    # 메타 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_mock = Column(Boolean, default=False)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    alert_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(String, nullable=False)

    building = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())