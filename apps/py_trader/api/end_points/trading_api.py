from fastapi import APIRouter, Depends

from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.data.repository.config_repo import ConfigRepo
from apps.py_trader.data.repository.place_order_request_doc_repo import PlaceOrderRequestDocRepo
from apps.py_trader.di import Container
from apps.py_trader.service.trading_service.trading_schema import PlaceOrderRequestCreate
from apps.py_trader.service.trading_service.trading_service import TradingService

trading_api = APIRouter(prefix= Routes.Trading.PREFIX, tags=['Trading'])


@trading_api.post(path=Routes.Trading.CreatePlaceOrderRequest, response_model=int)
async def create_place_order_request(
        request : PlaceOrderRequestCreate,
        config_repo: ConfigRepo = Depends(Container.configs_repo),
        place_order_doc_repo: PlaceOrderRequestDocRepo = Depends(Container.configs_repo),
        trading_service : TradingService = Depends(Container.trading_service),
):
    config = config_repo.read_last_config(raise_if_none= True)

    place_order_doc = trading_service.generate_place_order_request_doc(request, config)

    await place_order_doc_repo.create_one(place_order_doc)

    return 1
