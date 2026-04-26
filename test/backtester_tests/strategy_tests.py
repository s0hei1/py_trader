import pytest
from httpx import AsyncClient
from apps.backtester.api.router.routes import Routes
from global_fixture import async_client,app

@pytest.fixture
def strategy() -> dict:
    return {
        "description" : "Test Strategy",
        "setup_id" : 1,
        "risk_management_id" : 1,
    }

@pytest.mark.asyncio
async def test_create_strategy(async_client: AsyncClient, strategy: dict):
    response = await async_client.post(Routes.Strategy.PREFIX + Routes.Strategy.CreateOne,json=strategy)
    response.raise_for_status()

    data = response.json()
    assert strategy["description"] == data["description"]
    print(data)

@pytest.mark.asyncio
async def test_read_many_strategies(async_client: AsyncClient, strategy: dict):
    response = await async_client.post(Routes.Strategy.PREFIX + Routes.Strategy.ReadMany,json=strategy)
    response.raise_for_status()

    data = response.json()
    assert isinstance(data, list)
    print(data)


