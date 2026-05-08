from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Measurement
from schemas import MeasurementCreate, MeasurementResponse
from score_calculator import calculate_score_from_dict


router = APIRouter(prefix="/measurement")


ALLOWED_LOCATIONS = {
    "공학관": [2, 4, 5, 6],
    "학생회관": [1],
    "도서관": [4, 5],
}


@router.post("/", response_model=MeasurementResponse)
def create_measurement(data: MeasurementCreate, db: Session = Depends(get_db)):

    if data.building not in ALLOWED_LOCATIONS:
        raise HTTPException(
            status_code=400,
            detail="허용되지 않은 건물입니다. 공학관, 학생회관, 도서관만 선택할 수 있습니다."
        )

    floor = int(data.floor)

    if floor not in ALLOWED_LOCATIONS[data.building]:
        raise HTTPException(
            status_code=400,
            detail=f"{data.building}에서는 {ALLOWED_LOCATIONS[data.building]}층만 선택할 수 있습니다."
        )

    score_result = calculate_score_from_dict(data.dict())

    db_data = Measurement(
        ssid=data.ssid,
        bssid=data.bssid,
        rssi=data.rssi,
        latency=data.latency,
        building=data.building,
        floor=floor,
        location_name=data.location_name,

        download_speed=data.download_speed,
        link_speed=data.link_speed,

        score=score_result["score"],
        status=score_result["status"],

        is_mock=False,
        created_at=datetime.utcnow(),
    )

    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data


@router.get("", response_model=list[MeasurementResponse])
def get_measurements(db: Session = Depends(get_db)):
    measurements = (
        db.query(Measurement)
        .order_by(Measurement.created_at.desc())
        .all()
    )

    return measurements