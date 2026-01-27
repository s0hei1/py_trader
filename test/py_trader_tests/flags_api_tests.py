import pytest
from httpx import AsyncClient

from apps.py_trader.api.routing_helper.routes import Routes
from global_fixture import app, async_client

@pytest.mark.asyncio
async def test_read_flags_for_first_time(
    async_client: AsyncClient
):
    response = await async_client.get(Routes.Base.PREFIX + Routes.Base.FlagsRead)
    response.raise_for_status()

    data = response.json()
    print(data)
