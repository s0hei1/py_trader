from dataclasses import dataclass
from typing import Literal
from third_party.mt5_overhead.ordertype import OrderType

@dataclass
class TradeSignal:
    order_type : OrderType
    entry_price : float | None = None
    stop_loss_price : float | None = None
    take_profit_price : float | None = None
    external_trade_id : str | None = None


