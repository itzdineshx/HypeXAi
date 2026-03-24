from collections.abc import Generator

from pymongo import ASCENDING, MongoClient, ReturnDocument
from pymongo.database import Database

from app.core.config import get_settings

settings = get_settings()

mongo_client = MongoClient(settings.mongodb_uri)
mongo_db = mongo_client[settings.mongodb_db_name]


def SessionLocal() -> Database:
    return mongo_db


def get_db() -> Generator[Database, None, None]:
    yield mongo_db


def ping_db() -> None:
    mongo_client.admin.command("ping")


def close_mongo_client() -> None:
    mongo_client.close()


def get_next_sequence(name: str) -> int:
    counter = mongo_db["counters"].find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(counter["seq"])


def ensure_indexes(db: Database) -> None:
    db["coins"].create_index([("symbol", ASCENDING)], unique=True)
    db["alerts"].create_index([("id", ASCENDING)], unique=True)
    db["alerts"].create_index([("coin_symbol", ASCENDING), ("created_at", ASCENDING)])
    db["trend_points"].create_index([("coin_symbol", ASCENDING), ("ts", ASCENDING)])
    db["influencers"].create_index([("id", ASCENDING)], unique=True)
    db["influencers"].create_index([("handle", ASCENDING)], unique=True)
    db["influence_metrics"].create_index([("influencer_handle", ASCENDING), ("metric", ASCENDING)])
    db["replay_events"].create_index([("id", ASCENDING)], unique=True)
    db["social_posts"].create_index([("source", ASCENDING), ("post_id", ASCENDING)], unique=True)
