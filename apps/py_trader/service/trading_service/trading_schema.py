from pydantic import BaseModel


class PlaceOrderRequestCreate(BaseModel):
    order_type_id : int
    symbol_id : int
    volume : float
    entry_price : float
    stop_loss : float
    take_profit : float
    magic_id : int

class PlaceOrderRequestRead(BaseModel):
    place_status : bool
    order_mt5_id : int