import pytest
from httpx import AsyncClient
from apps.backtester.api.router.routes import Routes
from global_fixture import async_client,app

@pytest.mark.asyncio
async def test_read_many_MAs(async_client: AsyncClient):
    response = await async_client.get(Routes.MABacktesting.PREFIX + Routes.MABacktesting.ReadManyMAs)
    response.raise_for_status()

    data = response.json()
    assert isinstance(data, list)
    print(data)

