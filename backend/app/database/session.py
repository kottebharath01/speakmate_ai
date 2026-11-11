from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

db_url = settings.DATABASE_URL

# Normalize PostgreSQL URLs for SQLAlchemy
# Convert postgres:// or postgresql:// to postgresql+psycopg2:// if no driver is specified
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

# SQLite requires check_same_thread=False; PostgreSQL/Neon does not
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Crucial for Neon serverless PostgreSQL to recover from cold standby
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def ensure_schema_columns(target_engine):
    """
    Safely adds newly added columns to existing tables without dropping user data.
    Works across both SQLite and PostgreSQL.
    """
    inspector = inspect(target_engine)
    existing_tables = inspector.get_table_names()

    migrations = {
        "learning_profiles": [
            ("longest_streak", "INTEGER DEFAULT 0")
        ],
        "practice_attempts": [
            ("session_id", "INTEGER"),
            ("repetition_required", "BOOLEAN DEFAULT FALSE"),
            ("repetition_success_count", "INTEGER DEFAULT 0"),
            ("repetition_history_json", "TEXT"),
            ("item_completed", "BOOLEAN DEFAULT FALSE"),
        ],
        "word_items": [
            ("content_uid", "VARCHAR(120)"),
            ("mode", "VARCHAR(50)"),
            ("normalized_english", "VARCHAR(255)"),
            ("valid_alternatives_json", "TEXT"),
        ],
    }

    with target_engine.begin() as conn:
        for table_name, columns in migrations.items():
            if table_name not in existing_tables:
                continue
            existing_cols = {c["name"] for c in inspector.get_columns(table_name)}
            for col_name, col_def in columns:
                if col_name not in existing_cols:
                    conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def}"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
