from contextlib import contextmanager

from backend.infrastructure.orm.orm_base import Base
from backend.infrastructure.orm.orm_engine import SessionLocal, engine


@contextmanager
def session_scope():
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
