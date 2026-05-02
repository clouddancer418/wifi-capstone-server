from score_calculator import calculate_score_from_dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Measurement
from schemas import MeasurementCreate, MeasurementResponse
from score_calculator import calculate_score

router = APIRouter(prefix="/measurement")

@router.post("/", response_model=MeasurementResponse)
def create_measurement(data: MeasurementCreate, db: Session = Depends(get_db)):

    score_result = calculate_score_from_dict(data.dict())

    db_data = Measurement(
    ssid=data.ssid,
    bssid=data.bssid,
    rssi=data.rssi,
    latency=data.latency,
    building=data.building,
    download_speed=data.download_speed,
    link_speed=data.link_speed,
    score=score_result["score"],
    status=score_result["status"],

    is_mock=False,
    location_name=data.location_name,
    floor=data.floor
)

    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data