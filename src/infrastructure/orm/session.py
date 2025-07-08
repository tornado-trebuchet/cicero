from contextlib import contextmanager
from .engine import SessionLocal, engine
from .base import Base

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
