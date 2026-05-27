from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL=settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True if settings.ENVIRONMENT == "DEBUG" else False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass