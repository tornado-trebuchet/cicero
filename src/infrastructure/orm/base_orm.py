from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

metadata = MetaData()

class DatabaseConfig:
    def __init__(self, database_url: str) -> None:
        self.engine: Engine = create_engine(
            database_url, 
            echo=False,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600    # Recycle connections every hour
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
    
    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        return self.SessionLocal()