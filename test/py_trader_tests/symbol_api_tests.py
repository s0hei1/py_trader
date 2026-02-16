import pytest
from httpx import AsyncClient
from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client
from random import randint

@pytest.fixture
def symbol() -> dict:
    return {
        "base_currency": f"{randint(0,99)}GBP",
        "quote_currency": f"{randint(0,99)}USD"
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

@pytest.mark.asyncio
async def test_duplicate_symbol_name_should_not_creatable(
        async_client: AsyncClient,
        symbol : dict
):
    response = await async_client.post(Routes.Symbol.PREFIX + Routes.Symbol.CreateOne, json=symbol)
    response.raise_for_status()

    response_json = response.json()

    assert "id" in response_json
    response_json.pop("id")
    assert response_json == symbol

    response_duplicate = await async_client.post(Routes.Symbol.PREFIX + Routes.Symbol.CreateOne, json=symbol)
    assert response_duplicate.status_code == 400

