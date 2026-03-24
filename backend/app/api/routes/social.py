from fastapi import APIRouter, Depends, Query
from pymongo.database import Database

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas import SocialFetchRequest, SocialFetchResponse, SocialPostOut
from app.services.social_ingestion import fetch_and_store_social_data, list_social_posts

router = APIRouter()


@router.post("/fetch", response_model=SocialFetchResponse)
async def fetch_social_data(payload: SocialFetchRequest, db: Database = Depends(get_db)) -> SocialFetchResponse:
    settings = get_settings()
    result = await fetch_and_store_social_data(db=db, settings=settings, payload=payload)
    return result.response


@router.get("/posts", response_model=list[SocialPostOut])
def get_social_posts(
    source: str | None = Query(default=None, description="Filter by source: twitter or reddit"),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Database = Depends(get_db),
) -> list[SocialPostOut]:
    return list_social_posts(db=db, limit=limit, source=source)
