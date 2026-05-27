from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL_ASYNC=settings.DATABASE_URL_ASYNC

engine = create_async_engine(
    DATABASE_URL_ASYNC,
    echo = True if settings.ENVIRONMENT == "DEBUG" else False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass