from enum import Enum
import MetaTrader5 as mt5
from dataclasses import dataclass

@dataclass
class Action:
    name : str
    mt5_type: int


class ActionEnum:
    BUY = Action(name = "buy", mt5_type= mt5.ORDER_TYPE_BUY)
    SELL = Action(name = "sell", mt5_type= mt5.ORDER_TYPE_SELL)