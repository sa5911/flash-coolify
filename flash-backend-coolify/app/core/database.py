from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from urllib.parse import urlparse

_connect_args = {}
try:
    parsed = urlparse(settings.DATABASE_URL)
    if parsed.scheme.startswith("postgres"):
        hostname = parsed.hostname or ""
        _connect_args = {
            "connect_timeout": 30,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
        if "pooler.supabase.com" in hostname or hostname.endswith(".supabase.co"):
            _connect_args["options"] = "-c statement_timeout=10000"
    elif parsed.scheme.startswith("sqlite"):
        _connect_args = {"check_same_thread": False}
except Exception:
    _connect_args = {}

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    connect_args=_connect_args,
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
