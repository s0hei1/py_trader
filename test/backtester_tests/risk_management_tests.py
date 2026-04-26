import pytest
from httpx import AsyncClient
from apps.backtester.api.router.routes import Routes
from global_fixture import async_client,app
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def risk_management() -> dict:
    return {
        "description" : "Test Risk Management",
        "stop_loss_type" : 1,
        "stop_loss_size" : 20,
        "take_profit_size" : 20,
    }


@pytest.mark.asyncio
async def test_create_setup(async_client: AsyncClient, risk_management: dict):
    response = await async_client.post(Routes.RiskManagement.PREFIX + Routes.RiskManagement.CreateOne,json=risk_management)
    response.raise_for_status()

    data = response.json()
    assert risk_management["description"] == data["description"]
    print(data)

@pytest.mark.asyncio
async def test_read_many_setups(async_client: AsyncClient, risk_management: dict):
    response = await async_client.post(Routes.RiskManagement.PREFIX + Routes.RiskManagement.ReadMany,json=risk_management)
    response.raise_for_status()

    data = response.json()
    assert isinstance(data, list)
    print(data)


