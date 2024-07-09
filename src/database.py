# db connection related stuff
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)  # Use future=True for SQLAlchemy 2.0
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
