from pydantic import BaseModel
from datetime import datetime

class MeasurementCreate(BaseModel):
    ssid: str
    bssid: str
    rssi: int
    latency: float
    building: str
    download_speed: float | None = None
    link_speed: int | None = None
    location_name: str | None = None
    floor: str | None = None

class MeasurementResponse(BaseModel):
    id: int
    ssid: str
    rssi: int
    latency: float
    score: float
    status: str
    created_at: datetime
    download_speed: float | None = None
    link_speed: int | None = None
    is_mock: bool
    location_name: str | None = None
    floor: str | None = None

    class Config:
        from_attributes = True