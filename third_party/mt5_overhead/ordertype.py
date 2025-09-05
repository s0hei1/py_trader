from enum import Enum
from typing import ClassVar, Literal
from enum import Enum
import MetaTrader5 as mt5
from dataclasses import dataclass
from more_itertools import first


@dataclass
class OrderType:
    base_type: Literal['BUY', 'SELL']
    name: str
    mt5_type: int

    def is_buy(self):
        return self.base_type == "BUY"
    def is_sell(self):
        return self.base_type == "SELL"



class OrderTypes(Enum):
    buy_limit: ClassVar[OrderType] = OrderType(base_type="BUY", name="Buy Limit", mt5_type=mt5.ORDER_TYPE_BUY_LIMIT)
    sell_limit: ClassVar[OrderType] = OrderType(base_type="SELL", name="Sell Limit", mt5_type=mt5.ORDER_TYPE_SELL_LIMIT)

    @classmethod
    def get_type_names(cls) -> list[str]:
        return [i.value.name for i in cls]

    @classmethod
    def get_type_by_name(cls, input_name: str) -> OrderType:
        return first([i.value for i in cls if i.value.name == input_name])
