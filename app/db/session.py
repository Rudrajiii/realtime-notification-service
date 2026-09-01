import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/realtime_notification_service"
)

engine = create_async_engine(DATABASE_URL, echo=False)
session_local = async_sessionmaker(engine, expire_on_commit=False)



