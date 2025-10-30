from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True,  # Logging SQL queries
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
