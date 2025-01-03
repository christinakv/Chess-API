# core/models/db_helper.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

async def get_db_session():
    """Creates an asynchronous database session."""

    engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        yield session