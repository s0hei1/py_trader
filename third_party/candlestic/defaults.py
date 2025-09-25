from enum import Enum
from functools import lru_cache
from typing import Optional

import MetaTrader5 as mt5
from more_itertools import first

from third_party.candlestic.symbol import Symbol
from third_party.candlestic.time_frame import TimeFrame

class DefaultTimeFrames(Enum):
    M1 = TimeFrame(name="m1", mt5_value=mt5.TIMEFRAME_M1, included_m1=1)
    M5 = TimeFrame(name="m5", mt5_value=mt5.TIMEFRAME_M5, included_m1=5)
    M15 = TimeFrame(name="m15", mt5_value=mt5.TIMEFRAME_M15, included_m1=15)
    H1 = TimeFrame(name="h1", mt5_value=mt5.TIMEFRAME_H1, included_m1=60)
    H4 = TimeFrame(name="h4", mt5_value=mt5.TIMEFRAME_H4, included_m1=240)
    Daily = TimeFrame(name="daily", mt5_value=mt5.TIMEFRAME_D1, included_m1=1440)
    Weekly = TimeFrame(name="weekly", mt5_value=mt5.TIMEFRAME_W1, included_m1=10080)
    Monthly = TimeFrame(name="monthly", mt5_value=mt5.TIMEFRAME_MN1, included_m1=44640)

    @classmethod
    def get_time_frame_by_mt5_value(cls, mt5_value: int) -> 'TimeFrameEnum | None':
        return first([i for i in DefaultTimeFrames if i.value.mt5_value == mt5_value], default=None)

    @classmethod
    def get_time_frame_by_name(self, name: str) -> TimeFrame | None:
        return first([i.value for i in DefaultTimeFrames if i.value.name == name] , default=None)

    @classmethod
    def get_time_frame_names(cls):
        return [i.value.name for i in cls]

    @classmethod
    def get_enum_by_time_frame_obj(cls, time_frame : TimeFrame) -> Optional['DefaultTimeFrames']:
        return first([i for i in DefaultTimeFrames if i.value == time_frame], default=None)

    @property
    def trigger_time_dict(self) -> dict['DefaultTimeFrames','DefaultTimeFrames']:
        return {
            self.M15: self.M1,
            self.H1: self.M5,
            self.H4: self.M15,
            self.Daily: self.H1,
            self.Weekly: self.H4,
            self.Monthly: self.Daily,
        }



    @classmethod
    def get_trigger_time(cls, time_frame : TimeFrame) -> TimeFrame:
        enum_obj = cls.get_enum_by_time_frame_obj(time_frame)
        trigger_time_dict = enum_obj.trigger_time_dict
        return (trigger_time_dict[enum_obj]).value


class DefaultSymbols(Enum):
    eur_usd = Symbol("EUR","USD",0.0001)

    @classmethod
    def get_symbol_by_name(cls, symbol_name : str):
        return first((i.value for i in cls if i.value.symbol_name == symbol_name))

    @classmethod
    def get_symbols_name(cls):
        return [i.value.symbol_name for i in cls]