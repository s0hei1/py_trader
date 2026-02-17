import pytest
from httpx import AsyncClient
from sqlalchemy.exc import IntegrityError

from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client
from random import randint

@pytest.fixture
def pattern() -> dict:
    return {
        "pattern_group_id": 1,
        "pattern_first_candle": "2026-02-12T20:33:24.309Z",
        "pattern_last_candle": "2026-02-19T20:33:24.309Z",
        "is_active": True,
        "time_frame": "m1",
        "symbol_id": 1
    }

@pytest.fixture
def pattern_group() -> dict:
    return {
        "name": f"pivot{randint(1, 1000)}",
        "is_active": True,
    }


@pytest.mark.asyncio
async def test_create_pattern_successfully(
        async_client: AsyncClient,
        pattern: dict
):
    response = await async_client.post(Routes.Pattern.PREFIX + Routes.Pattern.Create, json=pattern)
    response.raise_for_status()

@pytest.mark.asyncio
async def test_create_pattern_group_successfully(
        async_client: AsyncClient,
        pattern_group: dict
):
    response = await async_client.post(Routes.Pattern.PREFIX + Routes.Pattern.CreateGroup, json=pattern_group)
    response.raise_for_status()

    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_crate_pattern_group_with_same_name_should_raise_exception(
        async_client: AsyncClient,
        pattern_group: dict
):
    response = await async_client.post(Routes.Pattern.PREFIX + Routes.Pattern.CreateGroup, json=pattern_group)
    response.raise_for_status()

    response_duplicate = await async_client.post(Routes.Pattern.PREFIX + Routes.Pattern.CreateGroup, json=pattern_group)
    assert response_duplicate.status_code == 400
    print(response_duplicate.json())

@pytest.mark.asyncio
async def test_read_many_pattern_groups(
        async_client: AsyncClient,
):
    response = await async_client.get(Routes.Pattern.PREFIX + Routes.Pattern.ReadManyGroups)
    response.raise_for_status()

    assert isinstance(response.json(), list)








