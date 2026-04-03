"""
Database Session Management
"""
from functools import lru_cache
from typing import Generator
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.settings import get_settings

logger = logging.getLogger(__name__)

@lru_cache()
def get_engine():
    settings = get_settings()
    
    # SQLite-specific configuration
    if "sqlite" in settings.DATABASE_URL:
        connect_args = {
            "check_same_thread": False,
            "timeout": 30  # 30 second timeout for database locks
        }
        # Use NullPool for SQLite to avoid connection pooling issues
        from sqlalchemy.pool import NullPool
        return create_engine(
            settings.DATABASE_URL,
            connect_args=connect_args,
            poolclass=NullPool,
            echo=settings.ENVIRONMENT == "development"
        )
    else:
        # PostgreSQL or other databases
        return create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            echo=settings.ENVIRONMENT == "development"
        )


@lru_cache()
def get_sessionmaker() -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


# Module-level SessionLocal for direct database access
SessionLocal: sessionmaker = get_sessionmaker()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    
    Usage in FastAPI:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database - create all tables
    """
    from app.database.base import Base, import_models
    
    # Import all models
    import_models()
    
    # Create all tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=get_engine())
    logger.info("✅ Database tables created successfully")
