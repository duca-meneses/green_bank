from typing import Generator
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from green_bank.infra.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

def get_session() -> Generator:
    with Session(engine) as session:
        yield session
