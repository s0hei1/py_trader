from enum import Enum
from functools import lru_cache
import MetaTrader5 as mt5
from more_itertools import first

from third_party.candlestic.symbol import Symbol
from third_party.candlestic.time_frame import TimeFrame

class TimeFrames(Enum):
    M1 = TimeFrame(name="m1", mt5_value=mt5.TIMEFRAME_M1, included_m1=1)
    M5 = TimeFrame(name="m5", mt5_value=mt5.TIMEFRAME_M5, included_m1=5)
    M15 = TimeFrame(name="m15", mt5_value=mt5.TIMEFRAME_M15, included_m1=15)
    H1 = TimeFrame(name="h1", mt5_value=mt5.TIMEFRAME_H1, included_m1=60)
    H4 = TimeFrame(name="h4", mt5_value=mt5.TIMEFRAME_H4, included_m1=240)
    Daily = TimeFrame(name="daily", mt5_value=mt5.TIMEFRAME_D1, included_m1=1440)
    Weekly = TimeFrame(name="weekly", mt5_value=mt5.TIMEFRAME_W1, included_m1=10080)
    Monthly = TimeFrame(name="monthly", mt5_value=mt5.TIMEFRAME_MN1, included_m1=43200)

    @classmethod
    @lru_cache
    def get_time_frame_by_mt5_value(cls, mt5_value: int) -> 'TimeFrameEnum | None':
        return first([i for i in TimeFrames if i.value.mt5_value == mt5_value], default=None)

    @classmethod
    @lru_cache
    def get_time_frame_by_name(self, name: str) -> 'TimeFrameEnum | None':
        return first([i for i in TimeFrames if i.value.name == name], default=None)

class Symbols(Enum):
    EURUSD = Symbol("EUR","USD",suffix="b")