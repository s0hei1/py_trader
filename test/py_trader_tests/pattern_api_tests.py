import pytest
from httpx import AsyncClient
from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client


@pytest.fixture
def pattern() -> dict:
    return {
        "pattern_group_id": 1,
        "pattern_first_candle": "2026-02-11T20:33:24.309Z",
        "pattern_last_candle": "2026-02-12T20:33:24.309Z",
        "is_active": True,
        "time_frame": "m1",
        "symbol_id": 1
    }

@pytest.mark.asyncio
async def test_create_pattern_successfully(
        async_client: AsyncClient,
        pattern: dict
):
    response = await async_client.post(Routes.Pattern.PREFIX + Routes.Pattern.Create, json=pattern)
    response.raise_for_status()

