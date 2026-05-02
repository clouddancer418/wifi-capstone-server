from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Alert

router = APIRouter()


@router.post("/report")
def report_wifi(
    building: str,
    message: str = "WiFi 불량 신고",
    db: Session = Depends(get_db)
):
    alert = Alert(
        alert_type="user_report",
        message=f"[사용자 신고] {building} - {message}",
        severity="medium",
        building=building,
        created_at=datetime.now()
    )

    db.add(alert)
    db.commit()

    return {
        "status": "ok",
        "message": "신고가 접수되었습니다."
    }


@router.post("/rating")
def submit_rating(
    building: str,
    rating: int,
    db: Session = Depends(get_db)
):
    if rating <= 2:
        alert = Alert(
            alert_type="low_rating",
            message=f"[낮은 평가] {building} - 사용자 평가 {rating}점",
            severity="medium",
            building=building,
            created_at=datetime.now()
        )

        db.add(alert)
        db.commit()

    return {
        "status": "ok",
        "rating": rating
    }