import pytest
from httpx import AsyncClient
from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client


@pytest.fixture
def config() -> dict:
    return {
        "maximum_risk_percentage": 2,
        "default_risk_percentage": 2,
        "total_balance": 2000
    }

@pytest.mark.asyncio
async def test_read_flags_for_first_time(
        async_client: AsyncClient
):
    response = await async_client.get(Routes.Base.PREFIX + Routes.Base.FlagsRead)
    response.raise_for_status()

    data = response.json()
    print(data)

@pytest.mark.asyncio
async def test_create_config_success(
        async_client: AsyncClient,
        config : dict
):
    response = await async_client.post(Routes.Base.PREFIX + Routes.Base.ConfigCreate, json=config)
    response.raise_for_status()

    response_json = response.json()

    assert "id" in response_json
    response_json.pop("id")
    assert response_json == config


@pytest.mark.asyncio
async def test_read_configs_history(
        async_client: AsyncClient
):
    response = await async_client.get(Routes.Base.PREFIX + Routes.Base.ConfigReadHistory)
    response.raise_for_status()

    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_last_config_must_equal_with_last_configs_history(
        async_client: AsyncClient
):
    configs_history_response = await async_client.get(Routes.Base.PREFIX + Routes.Base.ConfigReadHistory)
    configs_history_response.raise_for_status()

    last_config_response = await async_client.get(Routes.Base.PREFIX + Routes.Base.ConfigReadLast)
    last_config_response.raise_for_status()

    assert last_config_response.json() == configs_history_response.json()[0]

