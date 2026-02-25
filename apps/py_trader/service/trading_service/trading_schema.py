from pydantic import BaseModel

from apps.py_trader.data.enums.order_types_enum import OrderTypeEnum


class PlaceOrderRequestCreate(BaseModel):
    order_type : OrderTypeEnum
    symbol_id : int
    entry_price : float
    stop_loss : float
    take_profit : float
    magic_id : int
    risk_percentage : int | None = None

class PlaceOrderRequestRead(BaseModel):
    place_status : bool
    order_mt5_id : int