import pytest
from httpx import AsyncClient
from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client


@pytest.fixture
def config() -> dict:
    return {
        "pattern_group_id": 0,
        "pattern_first_candle": "2026-02-11T20:33:24.309Z",
        "pattern_last_candle": "2026-02-11T20:33:24.309Z",
        "is_active": True,
        "time_frame": "m1",
        "symbol_id": 0
    }
