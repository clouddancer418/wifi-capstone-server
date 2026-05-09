from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, or_
from datetime import timedelta

from database import get_db
from models import Measurement, Alert


router = APIRouter()

ALLOWED_BUILDINGS = [
    "공학관",
    "학생회관",
    "도서관",
    "실외/이동중",
    "자동측정",
]

DISPLAY_HOURS = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]


def real_data_filter():
    return or_(
        Measurement.is_mock == False,
        Measurement.is_mock.is_(None)
    )


def to_kst_string(dt):
    if not dt:
        return None
    return (dt + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")


def kst_hour_expr():
    return (extract("hour", Measurement.created_at) + 9) % 24


def score_to_status(score):
    if score >= 80:
        return "좋음"
    elif score >= 50:
        return "보통"
    else:
        return "나쁨"


@router.get("/buildings")
def get_building_stats(db: Session = Depends(get_db)):
    results = (
        db.query(
            Measurement.building,
            func.avg(Measurement.score).label("avg_score"),
            func.count(Measurement.id).label("measurement_count"),
            func.max(Measurement.created_at).label("latest_measured_at"),
        )
        .filter(
            real_data_filter(),
            Measurement.building.in_(ALLOWED_BUILDINGS),
        )
        .group_by(Measurement.building)
        .order_by(func.count(Measurement.id).desc())
        .all()
    )

    response = []

    for r in results:
        avg_score = round(float(r.avg_score or 0), 1)

        response.append({
            "building": r.building,
            "avg_score": avg_score,
            "status": score_to_status(avg_score),
            "measurement_count": r.measurement_count,
            "latest_measured_at": to_kst_string(r.latest_measured_at),
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
            real_data_filter(),
            Measurement.building == building,
        )
        .group_by(kst_hour)
        .order_by(kst_hour)
        .all()
    )

    return [
        {
            "hour": int(r.hour),
            "avg_score": round(float(r.avg_score or 0), 1),
            "count": r.count,
            "latest_measured_at": to_kst_string(r.latest_measured_at),
        }
        for r in results
    ]


@router.get("/floors")
def get_floor_stats(building: str, db: Session = Depends(get_db)):
    if building not in ALLOWED_BUILDINGS:
        raise HTTPException(status_code=400, detail="허용되지 않은 건물입니다.")

    floor_label = func.coalesce(Measurement.floor, "미입력")

    results = (
        db.query(
            floor_label.label("floor"),
            func.avg(Measurement.score).label("avg_score"),
            func.count(Measurement.id).label("count"),
            func.max(Measurement.created_at).label("latest_measured_at"),
        )
        .filter(
            real_data_filter(),
            Measurement.building == building,
        )
        .group_by(floor_label)
        .order_by(floor_label)
        .all()
    )

    return [
        {
            "building": building,
            "floor": str(r.floor),
            "avg_score": round(float(r.avg_score or 0), 1),
            "status": score_to_status(float(r.avg_score or 0)),
            "count": r.count,
            "latest_measured_at": to_kst_string(r.latest_measured_at),
        }
        for r in results
    ]


@router.get("/recent")
def get_recent_measurements(db: Session = Depends(get_db)):
    measurements = (
        db.query(Measurement)
        .filter(
            real_data_filter(),
            Measurement.building.in_(ALLOWED_BUILDINGS),
        )
        .order_by(Measurement.created_at.desc())
        .limit(100)
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