from pydantic import BaseModel
from datetime import datetime


class MeasurementCreate(BaseModel):
    ssid: str | None = None
    bssid: str | None = None
    rssi: int
    latency: float
    building: str

    download_speed: float | None = None
    link_speed: int | None = None

    location_name: str | None = None
    floor: int


class MeasurementResponse(BaseModel):
    id: int
    ssid: str | None = None
    bssid: str | None = None
    rssi: int
    latency: float
    building: str
    floor: int

    score: float
    status: str
    created_at: datetime

    download_speed: float | None = None
    link_speed: int | None = None

    is_mock: bool
    location_name: str | None = None

    class Config:
        from_attributes = True