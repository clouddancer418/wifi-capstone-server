from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from database import get_db
from models import Measurement, Alert
from datetime import timedelta


router = APIRouter()

ALLOWED_BUILDINGS = ["공학관", "학생회관", "도서관"]

ALLOWED_FLOORS = {
    "공학관": [2, 4, 5, 6],
    "학생회관": [1],
    "도서관": [4, 5],
}

ALLOWED_HOURS = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]


def to_kst_string(dt):
    if not dt:
        return None
    return (dt + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")


def kst_hour_expr():
    return (extract("hour", Measurement.created_at) + 9) % 24


@router.get("/buildings")
def get_building_stats(db: Session = Depends(get_db)):
    kst_hour = kst_hour_expr()

    results = (
        db.query(
            Measurement.building,
            func.avg(Measurement.score).label("avg_score"),
            func.count(Measurement.id).label("measurement_count"),
            func.max(Measurement.created_at).label("latest_measured_at"),
        )
        .filter(
            Measurement.is_mock == False,
            Measurement.building.in_(ALLOWED_BUILDINGS),
            kst_hour.in_(ALLOWED_HOURS),
        )
        .group_by(Measurement.building)
        .all()
    )

    response = []

    for r in results:
        avg_score = round(r.avg_score, 1)
        status = "좋음" if avg_score >= 80 else "보통" if avg_score >= 50 else "나쁨"

        response.append({
            "building": r.building,
            "avg_score": avg_score,
            "status": status,
            "measurement_count": r.measurement_count,
            "latest_measured_at": to_kst_string(r.latest_measured_at),
            "allowed_floors": ALLOWED_FLOORS.get(r.building, []),
        })

    return response


@router.get("/hourly")
def get_hourly_stats(building: str, db: Session = Depends(get_db)):
    if building not in ALLOWED_BUILDINGS:
        raise HTTPException(status_code=400, detail="허용되지 않은 건물입니다.")

    kst_hour = kst_hour_expr()

    results = (
        db.query(
            kst_hour.label("hour"),
            func.avg(Measurement.score).label("avg_score"),
            func.count(Measurement.id).label("count"),
            func.max(Measurement.created_at).label("latest_measured_at"),
        )
        .filter(
            Measurement.is_mock == False,
            Measurement.building == building,
            kst_hour.in_(ALLOWED_HOURS),
        )
        .group_by(kst_hour)
        .order_by(kst_hour)
        .all()
    )

    return [
        {
            "hour": int(r.hour),
            "avg_score": round(r.avg_score, 1),
            "count": r.count,
            "latest_measured_at": to_kst_string(r.latest_measured_at),
        }
        for r in results
    ]


@router.get("/floors")
def get_floor_stats(building: str, db: Session = Depends(get_db)):
    if building not in ALLOWED_BUILDINGS:
        raise HTTPException(status_code=400, detail="허용되지 않은 건물입니다.")

    kst_hour = kst_hour_expr()

    results = (
        db.query(
            Measurement.floor,
            func.avg(Measurement.score).label("avg_score"),
            func.count(Measurement.id).label("count"),
            func.max(Measurement.created_at).label("latest_measured_at"),
        )
        .filter(
            Measurement.is_mock == False,
            Measurement.building == building,
            Measurement.floor.in_(ALLOWED_FLOORS[building]),
            kst_hour.in_(ALLOWED_HOURS),
        )
        .group_by(Measurement.floor)
        .order_by(Measurement.floor)
        .all()
    )

    return [
        {
            "building": building,
            "floor": r.floor,
            "avg_score": round(r.avg_score, 1),
            "status": "좋음" if r.avg_score >= 80 else "보통" if r.avg_score >= 50 else "나쁨",
            "count": r.count,
            "latest_measured_at": to_kst_string(r.latest_measured_at),
        }
        for r in results
    ]


@router.get("/recent")
def get_recent_measurements(db: Session = Depends(get_db)):
    kst_hour = kst_hour_expr()

    measurements = (
        db.query(Measurement)
        .filter(
            Measurement.is_mock == False,
            Measurement.building.in_(ALLOWED_BUILDINGS),
            kst_hour.in_(ALLOWED_HOURS),
        )
        .order_by(Measurement.created_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": m.id,
            "building": m.building,
            "floor": m.floor,
            "ssid": m.ssid,
            "rssi": m.rssi,
            "latency": m.latency,
            "score": m.score,
            "status": m.status,
            "created_at": to_kst_string(m.created_at),
        }
        for m in measurements
    ]


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": alert.id,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "severity": alert.severity,
            "building": alert.building,
            "created_at": to_kst_string(alert.created_at),
        }
        for alert in alerts
    ]