from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from apps.py_trader.data.enums.place_order_status import PlaceOrderStatus
from apps.py_trader.data.models.models import PlaceOrderRequestDoc, Config, Symbol
from apps.py_trader.service.time_service.time_service import TimeService
from apps.py_trader.service.trading_service.trading_schema import PlaceOrderRequestCreate
from third_party import mt5_overhead

class TradingService:

    def __init__(self, session: AsyncSession, time_service: TimeService):
        self.session = session
        self.time_service = time_service

    async def generate_place_order_request_doc(self, request: PlaceOrderRequestCreate,
                                               config: Config) -> PlaceOrderRequestDoc:
        symbol_q = await self.session.execute(
            select(Symbol).where(Symbol.id == request.symbol_id)
        )
        symbol = symbol_q.scalar_one_or_none()

        if symbol is None:
            raise ValueError(f"There is no symbol with id {request.symbol_id}")

        mt5_result = mt5_overhead.set_pending_order(
            order_type=request.order_type.to_order_type(),
            symbol=symbol.to_thirdparty_symbol(),
            volume=self.get_volume_size(request.entry_price, request.stop_loss, config.default_risk_percentage),
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            take_profit=request.take_profit,
            external_id="test",
        )
        doc_code = await self.generate_document_code()

        return PlaceOrderRequestDoc(
            document_code=doc_code,
            creation_datetime=self.time_service.get_now(),
            place_status=PlaceOrderStatus.SUCCESS if mt5_result.is_success else PlaceOrderStatus.FAILED,
            trading_platform="test",

            entry_price=request.entry_price,
            stop_loss_price=request.stop_loss_price,
            take_profit_price=request.take_profit_price,
            volume=self.get_volume_size(
                request.entry_price,
                request.stop_loss_price,
                config.default_risk_percentage,
            ),
            expected_commission=0.1,
            risk_percentage=config.default_risk_percentage,
        )

    def get_volume_size(self, entry_price: float, stop_loss: float, risk_percentage: float):
        return 0.1

    async def generate_document_code(self) -> int:
        q_code = await self.session.execute(
            select(func.max(PlaceOrderRequestDoc.document_code))
        )
        code = q_code.scalar_one_or_none()

        if code is None:
            return 1000001
        else:
            return code + 1

