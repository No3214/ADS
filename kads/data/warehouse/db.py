from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from kads.core import load_env

env = load_env()

DATABASE_URL = env.get("DATABASE_URL")
if not DATABASE_URL:
    # Fallback to local SQLite in project root
    db_path = Path(__file__).resolve().parents[3] / "kads_warehouse.db"
    DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Iterator[Session]:
    """FastAPI bağımlılığı: DB oturumu üretir ve kapatır."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """SQLite/lokal geliştirme için tabloları oluşturur."""
    # Helper to create tables for SQLite/Local Dev (Alembic will handle migrations in Prod)
    Base.metadata.create_all(bind=engine)
