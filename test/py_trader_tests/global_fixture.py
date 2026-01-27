import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from apps.paperless.main import app as application


@pytest.fixture
def app() -> FastAPI:
    return application


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/",
    ) as client:
        yield client
