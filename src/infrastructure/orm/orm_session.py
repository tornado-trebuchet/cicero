from contextlib import contextmanager

from src.infrastructure.orm.orm_base import Base
from src.infrastructure.orm.orm_engine import SessionLocal, engine


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


def create_tables():
    Base.metadata.create_all(bind=engine)
