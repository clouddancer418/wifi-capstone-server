from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    ssid = Column(String)
    bssid = Column(String)
    rssi = Column(Integer)
    latency = Column(Float)
    building = Column(String)
    
    download_speed = Column(Float, nullable=True)
    link_speed = Column(Integer, nullable=True)


    score = Column(Float)
    status = Column(String)

    created_at = Column(DateTime, default=func.now())
    
    is_mock = Column(Boolean, default=False)
    location_name = Column(String, nullable=True)
    floor = Column(String, nullable=True)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)
    message = Column(String)
    severity = Column(String)
    building = Column(String)
    created_at = Column(DateTime)