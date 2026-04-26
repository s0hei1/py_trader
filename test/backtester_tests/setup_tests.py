import pytest
from httpx import AsyncClient
from apps.backtester.api.router.routes import Routes
from global_fixture import async_client,app

@pytest.fixture
def setup() -> dict:
    return {
        "description" : "Test Setup",
        "trigger_type" : 1,
        "line_a_id" : 7,
        "line_a_period" : 1,
        "line_b_id" : 7,
        "line_b_period" : 24,
    }


@pytest.mark.asyncio
async def test_create_setup(async_client: AsyncClient, setup: dict):
    response = await async_client.post(Routes.Setup.PREFIX + Routes.Setup.CreateOne,json=setup)
    response.raise_for_status()

    data = response.json()
    assert setup["description"] == data["description"]
    print(data)

@pytest.mark.asyncio
async def test_read_many_setups(async_client: AsyncClient, setup: dict):
    print(setup)
    response = await async_client.post(Routes.Setup.PREFIX + Routes.Setup.ReadMany,json=setup)
    response.raise_for_status()

    data = response.json()
    assert isinstance(data, list)
    print(data)


