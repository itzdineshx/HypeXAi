from fastapi import APIRouter, Depends, Query
from pymongo import DESCENDING
from pymongo.database import Database

from app.db.session import get_db
from app.schemas import CoinOut, DashboardSummary, TrendPointOut

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Database = Depends(get_db)) -> DashboardSummary:
    tracked_coins = db["coins"].count_documents({})

    coin_aggregate = list(
        db["coins"].aggregate(
            [
                {
                    "$group": {
                        "_id": None,
                        "average_hype_score": {"$avg": "$hype_score"},
                        "average_trust_score": {"$avg": "$trust_score"},
                        "market_sentiment": {"$avg": "$sentiment_score"},
                    }
                }
            ]
        )
    )
    coin_stats = coin_aggregate[0] if coin_aggregate else {}
    average_hype_score = float(coin_stats.get("average_hype_score", 0.0) or 0.0)
    average_trust_score = float(coin_stats.get("average_trust_score", 0.0) or 0.0)
    market_sentiment = float(coin_stats.get("market_sentiment", 0.0) or 0.0)

    active_alerts = db["alerts"].count_documents({"status": {"$in": ["active", "investigating"]}})

    return DashboardSummary(
        tracked_coins=tracked_coins,
        average_hype_score=round(float(average_hype_score), 2),
        average_trust_score=round(float(average_trust_score), 2),
        active_alerts=active_alerts,
        market_sentiment=round(float(market_sentiment), 2),
    )


@router.get("/trending", response_model=list[CoinOut])
def get_trending_coins(limit: int = Query(default=10, ge=1, le=100), db: Database = Depends(get_db)) -> list[CoinOut]:
    docs = list(db["coins"].find({}, {"_id": 0}).sort([("hype_score", DESCENDING), ("change_24h", DESCENDING)]).limit(limit))
    return [CoinOut(**doc) for doc in docs]


@router.get("/trend-chart", response_model=list[TrendPointOut])
def get_trend_chart(
    symbol: str | None = Query(default=None),
    limit: int = Query(default=40, ge=1, le=500),
    db: Database = Depends(get_db),
) -> list[TrendPointOut]:
    query: dict[str, str] = {}
    if symbol:
        query["coin_symbol"] = symbol.upper()
    docs = list(db["trend_points"].find(query, {"_id": 0}).sort("ts", DESCENDING).limit(limit))
    return [TrendPointOut(**doc) for doc in docs]
