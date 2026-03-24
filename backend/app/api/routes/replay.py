from fastapi import APIRouter, Depends, Query
from pymongo import DESCENDING
from pymongo.database import Database

from app.db.session import get_db
from app.schemas import ReplayEventOut

router = APIRouter()


@router.get("/events", response_model=list[ReplayEventOut])
def get_replay_events(
    symbol: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=300),
    db: Database = Depends(get_db),
) -> list[ReplayEventOut]:
    query: dict[str, str] = {}
    if symbol:
        query["coin_symbol"] = symbol.upper()
    docs = list(db["replay_events"].find(query, {"_id": 0}).sort("occurred_at", DESCENDING).limit(limit))
    return [ReplayEventOut(**doc) for doc in docs]
