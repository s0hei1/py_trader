import pytest
from httpx import AsyncClient
from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client


@pytest.fixture
def symbol() -> dict:
    return {
        "base_currency": "GBP",
        "quote_currency": "USD"
    }


@pytest.mark.asyncio
async def test_create_config_success(
        async_client: AsyncClient,
        symbol : dict
):
    response = await async_client.post(Routes.Symbol.PREFIX + Routes.Symbol.CreateOne, json=symbol)
    response.raise_for_status()

    response_json = response.json()

    assert "id" in response_json
    response_json.pop("id")
    assert response_json == symbol
