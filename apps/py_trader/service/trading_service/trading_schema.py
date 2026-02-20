from pydantic import BaseModel



def PlaceOrderRequest():
    order_type_id : int
    symbol_id : int
    volume : float
    entry_price : float
    stop_loss : float
    take_profit : float
    magic_id : int

def PlaceOrderRequestResponse():
    place_status : bool
    order_mt5_id : int