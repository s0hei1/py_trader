from sqlalchemy.ext.asyncio import AsyncSession

from apps.py_trader.data.models.models import PlaceOrderRequestDoc
from apps.py_trader.service.trading_service.trading_schema import PlaceOrderRequestCreate
from third_party import mt5_overhead

class TradingService:

    def __init__(self, session : AsyncSession):
        self.session = session


    def generate_place_order_request_doc(self, request : PlaceOrderRequestCreate) -> PlaceOrderRequestDoc:





        return PlaceOrderRequestDoc(

        )

