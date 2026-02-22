from sqlalchemy.ext.asyncio import AsyncSession

from apps.py_trader.service.trading_service.trading_schema import PlaceOrderRequestCreate
from third_party import mt5_overhead

class TradingService:

    def __init__(self, session : AsyncSession):
        self.session = session


    def place_order(self, request : PlaceOrderRequestCreate):



        mt5_overhead.set_pending_order()

