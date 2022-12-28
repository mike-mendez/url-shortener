from ..models import url_model
from sqlmodel import create_engine, select, Session, SQLModel
from typing import Generator


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@database:5432/url_shortener"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session
