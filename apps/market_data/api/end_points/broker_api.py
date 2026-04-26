from fastapi import APIRouter, Depends
from apps.market_data.api.routes.routes import Routes
from apps.market_data.di import Container
from apps.market_data.data.repository import BrokerRepo
from apps.market_data.service.broker_schema import BrokerRead, BrokerCreate


broker_api_router = APIRouter(prefix=Routes.Broker.PREFIX, tags=["Brokers"])

@broker_api_router.post(Routes.Broker.CreateOne, response_model=BrokerRead)
async def create_broker(
    payload: BrokerCreate,
    broker_repo: BrokerRepo = Depends(Container.broker_repo)
):
    return await broker_repo.create_one(payload.to_broker())

@broker_api_router.get(Routes.Broker.ReadMany, response_model=list[BrokerRead])
async def list_brokers(
    broker_repo: BrokerRepo = Depends(Container.broker_repo)
):
    return await broker_repo.read_many()