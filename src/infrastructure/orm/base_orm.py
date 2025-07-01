from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import DatabaseConfig
from contextlib import contextmanager

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

metadata = MetaData()

config = DatabaseConfig()

engine = create_engine(
    config.database_url,
    echo=config.echo,
    pool_pre_ping=config.pool_pre_ping,
    pool_recycle=config.pool_recycle,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()