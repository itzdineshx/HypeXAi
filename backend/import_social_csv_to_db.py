import csv
from datetime import datetime
from pathlib import Path

from pymongo import UpdateOne
from pymongo.database import Database

from app.db.session import SessionLocal


def _parse_datetime(raw: str) -> datetime:
    text = (raw or "").strip()
    if not text:
        return datetime.utcnow()
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
    return datetime.utcnow()


def _to_int(raw: str) -> int:
    try:
        return int(float((raw or "0").strip()))
    except ValueError:
        return 0


def _to_float(raw: str) -> float:
    try:
        return float((raw or "0").strip())
    except ValueError:
        return 0.0


def _load_rows(csv_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            source = str(row.get("source", "")).strip().lower()
            post_id = str(row.get("post_id", "")).strip()
            if not source or not post_id:
                continue
            rows.append(
                {
                    "source": source,
                    "post_id": post_id,
                    "author": str(row.get("author", "")).strip(),
                    "context": str(row.get("context", "")).strip(),
                    "text": str(row.get("text", "")).strip(),
                    "coin_symbol": str(row.get("coin_symbol", "")).strip().upper(),
                    "influencer_handle": str(row.get("influencer_handle", "")).strip(),
                    "engagement_score": _to_int(str(row.get("engagement_score", "0"))),
                    "sentiment_compound": _to_float(str(row.get("sentiment_compound", "0"))),
                    "created_at": _parse_datetime(str(row.get("created_at", ""))),
                }
            )
    return rows


def _upsert(db: Database, rows: list[dict[str, object]]) -> tuple[int, int]:
    operations = [
        UpdateOne(
            {"source": str(row["source"]), "post_id": str(row["post_id"])},
            {"$set": row},
            upsert=True,
        )
        for row in rows
    ]
    if not operations:
        return 0, 0

    result = db["social_posts"].bulk_write(operations, ordered=False)
    inserted = int(result.upserted_count)
    updated = int(max(0, result.matched_count - result.upserted_count))
    return inserted, updated


def main() -> None:
    base_dir = Path("exports/social")
    files = [base_dir / "twitter_2026-03-24.csv", base_dir / "reddit_2026-03-24.csv"]

    rows: list[dict[str, object]] = []
    for file_path in files:
        if not file_path.exists():
            print(f"Missing file: {file_path}")
            continue
        rows.extend(_load_rows(file_path))

    if not rows:
        print("No rows to import.")
        return

    db = SessionLocal()
    inserted, updated = _upsert(db, rows)

    print(f"Rows imported: {len(rows)}")
    print(f"Inserted     : {inserted}")
    print(f"Updated      : {updated}")


if __name__ == "__main__":
    main()
