from app.db.init_db import seed_database
from app.db.session import SessionLocal, ensure_indexes, ping_db
from app.services.model_training import train_all_models


def main() -> None:
    ping_db()
    db = SessionLocal()
    ensure_indexes(db)
    seed_database(db)
    result = train_all_models(db)

    print("Training complete. Saved artifacts:")
    for model_name, metadata in result.items():
        artifact = metadata.get("artifact", "n/a")
        print(f"- {model_name}: {artifact}")


if __name__ == "__main__":
    main()