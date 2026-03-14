from sqlalchemy import create_engine # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker, declarative_base # pyright: ignore[reportMissingImports]

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()