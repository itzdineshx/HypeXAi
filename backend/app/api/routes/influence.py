import math

from fastapi import APIRouter, Depends, Query
from pymongo import DESCENDING
from pymongo.database import Database

from app.db.session import get_db
from app.schemas import InfluenceMetricOut, InfluencerOut

router = APIRouter()


@router.get("/top", response_model=list[InfluencerOut])
def get_top_influencers(
    category: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Database = Depends(get_db),
) -> list[InfluencerOut]:
    query: dict[str, str] = {}
    if category:
        query["category"] = category
    docs = list(db["influencers"].find(query, {"_id": 0}).sort("impact_score", DESCENDING).limit(limit))
    return [InfluencerOut(**doc) for doc in docs]


@router.get("/metrics", response_model=list[InfluenceMetricOut])
def get_influence_metrics(db: Database = Depends(get_db)) -> list[InfluenceMetricOut]:
    docs = list(db["influence_metrics"].find({}, {"_id": 0}))
    return [InfluenceMetricOut(**doc) for doc in docs]


@router.get("/radar")
def get_influence_radar(db: Database = Depends(get_db)) -> list[dict[str, int | str | float]]:
    influencers = list(db["influencers"].find({}, {"_id": 0}).sort("impact_score", DESCENDING).limit(15))
    if not influencers:
        return []

    points = []
    max_followers = max(int(influencer["followers"]) for influencer in influencers)

    for index, influencer in enumerate(influencers, start=1):
        # Blend impact/trust/activity into a single quality score for node emphasis.
        normalized_activity = min(100.0, float(influencer["posts_24h"]) / 2.4)
        quality_score = round(
            (float(influencer["impact_score"]) * 0.5)
            + (float(influencer["trust_score"]) * 0.35)
            + (normalized_activity * 0.15),
            1,
        )

        # Spread nodes radially by trust and angle by rank to avoid overlap.
        radius = 18.0 + ((100.0 - float(influencer["trust_score"])) / 100.0) * 30.0
        angle = (index * 360.0 / max(1, len(influencers))) + (index * 7.0)
        x = 50.0 + (radius * math.cos(math.radians(angle)))
        y = 50.0 + (radius * math.sin(math.radians(angle)))

        followers_ratio = float(influencer["followers"]) / max(1.0, float(max_followers))
        node_size = int(round(18.0 + (followers_ratio * 20.0) + (float(influencer["impact_score"]) / 10.0)))

        if quality_score >= 85:
            tier = "alpha"
        elif quality_score >= 70:
            tier = "core"
        elif quality_score >= 55:
            tier = "watch"
        else:
            tier = "risk"

        points.append(
            {
                "id": int(influencer.get("id", index)),
                "name": str(influencer["name"]),
                "handle": str(influencer["handle"]),
                "x": round(max(8.0, min(92.0, x)), 2),
                "y": round(max(8.0, min(92.0, y)), 2),
                "size": max(16, min(46, node_size)),
                "impact_score": int(influencer["impact_score"]),
                "trust_score": int(influencer["trust_score"]),
                "posts_24h": int(influencer["posts_24h"]),
                "followers": int(influencer["followers"]),
                "category": str(influencer["category"]),
                "quality_score": quality_score,
                "tier": tier,
            }
        )
    return points
