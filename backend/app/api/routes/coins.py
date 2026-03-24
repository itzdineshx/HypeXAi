from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo import DESCENDING
from pymongo.database import Database

from app.db.session import get_db
from app.schemas import AlertOut, CoinDetailOut, CoinOut, CoinRealtimeOut, DexPairOut, DexTokenProfileOut, InfluencerOut
from app.services.dexscreener import fetch_realtime_coin_snapshot, market_mood_emoji

router = APIRouter()


@router.get("", response_model=list[CoinOut])
def list_coins(
    search: str | None = Query(default=None),
    min_hype_score: int | None = Query(default=None, ge=0, le=100),
    limit: int = Query(default=50, ge=1, le=200),
    db: Database = Depends(get_db),
) -> list[CoinOut]:
    query: dict[str, object] = {}
    if search:
        escaped = search.strip()
        query["$or"] = [{"symbol": {"$regex": escaped, "$options": "i"}}, {"name": {"$regex": escaped, "$options": "i"}}]
    if min_hype_score is not None:
        query["hype_score"] = {"$gte": min_hype_score}
    docs = list(db["coins"].find(query, {"_id": 0}).sort("hype_score", DESCENDING).limit(limit))
    return [CoinOut(**doc) for doc in docs]


@router.get("/{symbol}", response_model=CoinDetailOut)
def get_coin(symbol: str, db: Database = Depends(get_db)) -> CoinDetailOut:
    coin = db["coins"].find_one({"symbol": symbol.upper()}, {"_id": 0})
    if not coin:
        raise HTTPException(status_code=404, detail=f"Coin '{symbol}' not found")

    snapshot = fetch_realtime_coin_snapshot(symbol=str(coin["symbol"]))
    pair_payload = snapshot.get("dex_pair")
    profile_payload = snapshot.get("dex_profile")
    dex_pair = DexPairOut(**pair_payload) if pair_payload else None
    dex_profile = DexTokenProfileOut(**profile_payload) if profile_payload else None

    price_change = (
        dex_pair.price_change_h24 if dex_pair and dex_pair.price_change_h24 is not None else float(coin["change_24h"])
    )
    mood_emoji = market_mood_emoji(price_change, int(coin["trust_score"]), int(coin["hype_score"]))

    return CoinDetailOut(
        symbol=str(coin["symbol"]),
        name=str(coin["name"]),
        price=dex_pair.price_usd if dex_pair and dex_pair.price_usd is not None else float(coin["price"]),
        market_cap=dex_pair.market_cap if dex_pair and dex_pair.market_cap is not None else float(coin["market_cap"]),
        volume_24h=dex_pair.volume_h24 if dex_pair and dex_pair.volume_h24 is not None else float(coin["volume_24h"]),
        change_24h=price_change,
        hype_score=int(coin["hype_score"]),
        trust_score=int(coin["trust_score"]),
        sentiment_score=int(coin["sentiment_score"]),
        prediction=str(coin["prediction"]),
        prediction_confidence=int(coin["prediction_confidence"]),
        risk_level=str(coin["risk_level"]),
        dex_pair=dex_pair,
        dex_profile=dex_profile,
        emoji=snapshot.get("emoji") or "\U0001FA99",
        market_emoji=mood_emoji,
        price_source="dexscreener" if dex_pair else "local_db",
        last_updated=datetime.utcnow(),
    )


@router.get("/{symbol}/realtime", response_model=CoinRealtimeOut)
def get_coin_realtime(symbol: str, db: Database = Depends(get_db)) -> CoinRealtimeOut:
    coin = db["coins"].find_one({"symbol": symbol.upper()}, {"_id": 0})
    if not coin:
        raise HTTPException(status_code=404, detail=f"Coin '{symbol}' not found")

    snapshot = fetch_realtime_coin_snapshot(symbol=str(coin["symbol"]))
    pair_payload = snapshot.get("dex_pair")
    profile_payload = snapshot.get("dex_profile")
    top_pairs_payload = snapshot.get("top_pairs") or []

    dex_pair = DexPairOut(**pair_payload) if pair_payload else None
    dex_profile = DexTokenProfileOut(**profile_payload) if profile_payload else None
    top_pairs = [DexPairOut(**pair) for pair in top_pairs_payload]

    price_change = (
        dex_pair.price_change_h24 if dex_pair and dex_pair.price_change_h24 is not None else float(coin["change_24h"])
    )
    mood_emoji = market_mood_emoji(price_change, int(coin["trust_score"]), int(coin["hype_score"]))

    return CoinRealtimeOut(
        symbol=str(coin["symbol"]),
        name=str(coin["name"]),
        price=dex_pair.price_usd if dex_pair and dex_pair.price_usd is not None else float(coin["price"]),
        market_cap=dex_pair.market_cap if dex_pair and dex_pair.market_cap is not None else float(coin["market_cap"]),
        volume_24h=dex_pair.volume_h24 if dex_pair and dex_pair.volume_h24 is not None else float(coin["volume_24h"]),
        change_24h=price_change,
        hype_score=int(coin["hype_score"]),
        trust_score=int(coin["trust_score"]),
        sentiment_score=int(coin["sentiment_score"]),
        prediction=str(coin["prediction"]),
        prediction_confidence=int(coin["prediction_confidence"]),
        risk_level=str(coin["risk_level"]),
        dex_pair=dex_pair,
        dex_profile=dex_profile,
        top_pairs=top_pairs,
        emoji=snapshot.get("emoji") or "\U0001FA99",
        market_emoji=mood_emoji,
        price_source="dexscreener" if dex_pair else "local_db",
        last_updated=datetime.utcnow(),
    )


@router.get("/{symbol}/alerts", response_model=list[AlertOut])
def get_coin_alerts(
    symbol: str,
    limit: int = Query(default=20, ge=1, le=100),
    db: Database = Depends(get_db),
) -> list[AlertOut]:
    docs = list(
        db["alerts"]
        .find({"coin_symbol": symbol.upper()}, {"_id": 0})
        .sort("created_at", DESCENDING)
        .limit(limit)
    )
    return [AlertOut(**doc) for doc in docs]


@router.get("/{symbol}/influencers", response_model=list[InfluencerOut])
def get_coin_influencers(symbol: str, db: Database = Depends(get_db)) -> list[InfluencerOut]:
    # Temporary signal: return top influencers for tracked symbols.
    coin_exists = db["coins"].find_one({"symbol": symbol.upper()}, {"symbol": 1})
    if not coin_exists:
        raise HTTPException(status_code=404, detail=f"Coin '{symbol}' not found")
    docs = list(db["influencers"].find({}, {"_id": 0}).sort("impact_score", DESCENDING).limit(10))
    return [InfluencerOut(**doc) for doc in docs]
