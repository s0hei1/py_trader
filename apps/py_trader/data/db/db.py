from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from apps.paperless.di import GeneralDI
from apps.paperless.data.db.read_only_async_session import ReadOnlyAsyncSession


def get_engine(url=GeneralDI.settings().development_db) -> AsyncEngine:
    return create_async_engine(url, echo=True)


def get_session(engine=get_engine(), class_=AsyncSession) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=False, class_=class_)


AsyncSessionLocal = get_session()
ReadOnlyAsyncSession = get_session(class_=ReadOnlyAsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_read_only_db():
    async with ReadOnlyAsyncSession() as session:
        yield session
