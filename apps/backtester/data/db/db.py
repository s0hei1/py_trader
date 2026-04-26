from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from apps.backtester.data.config.settings import Settings

def get_engine(url=Settings().database_url) -> AsyncEngine:

    return create_async_engine(url, echo=True)


def get_session(engine=get_engine(), class_=AsyncSession) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=False, class_=class_)


AsyncSessionLocal = get_session()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

