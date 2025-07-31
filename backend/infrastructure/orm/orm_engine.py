from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import DatabaseConfig

config = DatabaseConfig()

engine = create_engine(
    config.database_url,
    echo=config.echo,
    pool_pre_ping=config.pool_pre_ping,
    pool_recycle=config.pool_recycle,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
