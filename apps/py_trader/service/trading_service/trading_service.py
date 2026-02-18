from sqlalchemy.ext.asyncio import AsyncSession
from third_party import mt5_overhead

class TradingService:

    def __init__(self, session : AsyncSession):
        self.session = session


    def place_order(self):

        mt5_overhead.set_pending_order()

