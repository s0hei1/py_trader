from fastapi import APIRouter, Depends

from apps.py_trader.api.routing_helper.routes import Routes
from apps.py_trader.service.trading_service.trading_schema import PlaceOrderRequestCreate

trading_api = APIRouter(prefix= Routes.Trading.PREFIX, tags=['Trading'])


@trading_api.post(path=Routes.Trading.CreatePlaceOrderRequest, response_model=int)
async def create_place_order_request(pattern_create : PlaceOrderRequestCreate,):

    return 1
