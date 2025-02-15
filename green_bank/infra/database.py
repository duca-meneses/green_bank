from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from green_bank.infra.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
