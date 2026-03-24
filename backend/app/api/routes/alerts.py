from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo import DESCENDING
from pymongo.database import Database

from app.db.session import get_db, get_next_sequence
from app.schemas import AlertCreate, AlertOut, AlertStatusUpdate

router = APIRouter()


@router.get("", response_model=list[AlertOut])
def list_alerts(
    severity: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Database = Depends(get_db),
) -> list[AlertOut]:
    query: dict[str, str] = {}
    if severity:
        query["severity"] = severity
    if status:
        query["status"] = status

    docs = list(db["alerts"].find(query, {"_id": 0}).sort("created_at", DESCENDING).limit(limit))
    return [AlertOut(**doc) for doc in docs]


@router.post("", response_model=AlertOut, status_code=201)
def create_alert(payload: AlertCreate, db: Database = Depends(get_db)) -> AlertOut:
    alert = {
        "id": get_next_sequence("alerts"),
        "type": payload.type,
        "title": payload.title,
        "coin_symbol": payload.coin_symbol.upper(),
        "message": payload.message,
        "severity": payload.severity,
        "status": payload.status,
        "created_at": datetime.utcnow(),
    }
    db["alerts"].insert_one(alert)
    return AlertOut(**alert)


@router.patch("/{alert_id}/status", response_model=AlertOut)
def update_alert_status(alert_id: int, payload: AlertStatusUpdate, db: Database = Depends(get_db)) -> AlertOut:
    alert = db["alerts"].find_one({"id": alert_id}, {"_id": 0})
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found")

    db["alerts"].update_one({"id": alert_id}, {"$set": {"status": payload.status}})
    alert["status"] = payload.status
    return AlertOut(**alert)
