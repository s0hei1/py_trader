from __future__ import annotations
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



class OrderTypes:
    buy_limit: ClassVar[OrderType] = OrderType(base_type="BUY", name="Buy Limit", mt5_type=mt5.ORDER_TYPE_BUY_LIMIT)
    sell_limit: ClassVar[OrderType] = OrderType(base_type="SELL", name="Sell Limit", mt5_type=mt5.ORDER_TYPE_SELL_LIMIT)

    @classmethod
    def get_order_types(cls) -> list[OrderType]:
        return [
            getattr(cls, i)
            for i in OrderType.__annotations__
            if isinstance(getattr(cls, i), OrderType)
        ]


    @classmethod
    def get_type_names(self) -> list[str]:
        return [i.name for i in self.get_order_types()]

    @classmethod
    def get_type_by_name(self, input_name: str) -> OrderType:
        return first([i for i in self.get_order_types() if i.name == input_name])

