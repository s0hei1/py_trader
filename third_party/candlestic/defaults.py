from __future__ import annotations
from enum import Enum
from typing import Optional, Sequence
import MetaTrader5 as mt5
from more_itertools import first
from typing import Iterable
from third_party.candlestic.symbol import Symbol
from third_party.candlestic.time_frame import TimeFrame


class ClassicFractalTimeFrames:
    M1: TimeFrame = TimeFrame(name="m1", mt5_value=mt5.TIMEFRAME_M1, included_m1=1, fractal_value=15)
    M5: TimeFrame = TimeFrame(name="m5", mt5_value=mt5.TIMEFRAME_M5, included_m1=5, fractal_value=12)
    M15: TimeFrame = TimeFrame(name="m15", mt5_value=mt5.TIMEFRAME_M15, included_m1=15, fractal_value=16)
    H1: TimeFrame = TimeFrame(name="h1", mt5_value=mt5.TIMEFRAME_H1, included_m1=60, fractal_value=24)
    H4: TimeFrame = TimeFrame(name="h4", mt5_value=mt5.TIMEFRAME_H4, included_m1=240, fractal_value=30)
    Daily: TimeFrame = TimeFrame(name="daily", mt5_value=mt5.TIMEFRAME_D1, included_m1=1440, fractal_value=26)
    Weekly: TimeFrame = TimeFrame(name="weekly", mt5_value=mt5.TIMEFRAME_W1, included_m1=10080, fractal_value=52)
    Monthly: TimeFrame = TimeFrame(name="monthly", mt5_value=mt5.TIMEFRAME_MN1, included_m1=44640, fractal_value=12)

    _trigger_time_dict: dict[TimeFrame, TimeFrame] = {
        M15: M1,
        H1: M5,
        H4: M15,
        Daily: H1,
        Weekly: H4,
        Monthly: Daily,
    }

    _struct_time_dict: dict[TimeFrame, TimeFrame] = {
        M1: M15,
        M5: H1,
        M15: H4,
        H1: Daily,
        H4: Weekly,
        Daily: Monthly,
    }

    @classmethod
    def get_time_frames(cls) -> list[TimeFrame]:
        return [
            getattr(cls, i)
            for i in ClassicFractalTimeFrames.__annotations__
            if isinstance(getattr(cls, i), TimeFrame)
        ]

    @classmethod
    def get_time_frame_by_mt5_value(cls, mt5_value: int) -> TimeFrame | None:
        return first([i for i in cls.get_time_frames() if i.mt5_value == mt5_value], default=None)

    @classmethod
    def get_time_frame_by_name(cls, name: str) -> TimeFrame | None:
        return first([i for i in cls.get_time_frames() if i.name == name], default=None)

    @classmethod
    def get_time_frame_names(cls):
        return [i.name for i in cls.get_time_frames()]

    @classmethod
    def get_enum_by_time_frame_obj(cls, time_frame: TimeFrame) -> ClassicFractalTimeFrames | None:
        return first([i for i in cls.get_time_frames() if i == time_frame], default=None)

    @classmethod
    def get_trigger_time(cls, time_frame: TimeFrame) -> TimeFrame:
        return cls._trigger_time_dict[time_frame]



class DefaultSymbols:
    eur_usd : Symbol = Symbol("EUR", "USD", 4)

    @classmethod
    def get_symbols(cls) -> list[Symbol]:
        return [
            getattr(cls, i)
            for i in DefaultSymbols.__annotations__
            if isinstance(getattr(cls, i), Symbol)
        ]

    @classmethod
    def get_symbol_by_name(cls, symbol_name: str) -> Symbol | None:
        return first((i for i in cls.get_symbols() if i.symbol_name == symbol_name.upper()), default=None)

    @classmethod
    def get_symbols_name(cls) -> list[str]:
        return [i.symbol_name for i in cls.get_symbols()]

