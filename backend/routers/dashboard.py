from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from database import get_db
from models import Measurement
from models import Alert

router = APIRouter()

@router.get("/buildings")
def get_building_stats(db: Session = Depends(get_db)):
    results = db.query(
        Measurement.building,
        func.avg(Measurement.score).label("avg_score"),
        func.count(Measurement.id).label("measurement_count")
    ).group_by(
        Measurement.building
    ).all()

    response = []
    for r in results:
        avg_score = round(r.avg_score, 1)
        status = "좋음" if avg_score >= 80 else "보통" if avg_score >= 50 else "나쁨"

        response.append({
            "building": r.building,
            "avg_score": avg_score,
            "status": status,
            "measurement_count": r.measurement_count
        })

    return response


@router.get("/hourly")
def get_hourly_stats(building: str, db: Session = Depends(get_db)):
    results = db.query(
        extract("hour", Measurement.created_at).label("hour"),
        func.avg(Measurement.score).label("avg_score"),
        func.count(Measurement.id).label("count")
    ).filter(
        Measurement.building == building
    ).group_by(
        extract("hour", Measurement.created_at)
    ).order_by("hour").all()

    return [
        {
            "hour": int(r.hour),
            "avg_score": round(r.avg_score, 1),
            "count": r.count
        }
        for r in results
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
            "created_at": alert.created_at.isoformat() if alert.created_at else None,
        }
        for alert in alerts
    ]
