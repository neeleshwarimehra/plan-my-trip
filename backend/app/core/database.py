
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.engine import URL

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

database_url = make_url(DATABASE_URL)

def create_database_if_not_exists() -> None:
    target_database = database_url.database

    if not target_database:
        raise RuntimeError("Database name is missing.")

    admin_url = database_url.set(database="postgres")

    admin_engine = create_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin_engine.connect() as connection:
            exists = connection.execute(
                text(
                    "SELECT 1 FROM pg_database WHERE datname = :name"
                ),
                {"name": target_database},
            ).scalar()

            if not exists:
                quoted_name = (
                    connection.dialect.identifier_preparer
                    .quote_identifier(target_database)
                )
                connection.execute(
                    text(f"CREATE DATABASE {quoted_name}")
                )
                print(f"Database '{target_database}' created.")
            else:
                print(f"Database '{target_database}' already exists.")
    finally:
        admin_engine.dispose()


create_database_if_not_exists()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
