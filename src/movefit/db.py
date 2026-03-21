from contextlib import contextmanager
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./movefit.db"


def get_engine(database_url: str | None = None):
    if database_url is None:
        database_url = DATABASE_URL

    return create_engine(
        database_url,
        echo=False,
        connect_args={"check_same_thread": False},
    )


def create_db_and_tables(engine=None):
    if engine is None:
        engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel session to use as FastAPI dependency."""
    engine = get_engine()

    with Session(engine) as session:
        yield session
