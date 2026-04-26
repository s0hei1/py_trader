from typing import ClassVar
import talib
from apps.backtester.data.data_models import Line

class BacktesterLines:
    Close: Line = Line(id=1, name='SMA', line_type='PRICE', function=None)
    Open: Line = Line(id=2, name='SMA', line_type='PRICE', function=None)
    High: Line = Line(id=3, name='SMA', line_type='PRICE', function=None)
    Low: Line = Line(id=4, name='SMA', line_type='PRICE', function=None)
    Volume: Line = Line(id=5, name='SMA', line_type='PRICE', function=None)
    ATR: Line = Line(id=6, name='SMA', line_type='TRUE_RANGE', function=talib.ATR)
    SMA: Line = Line(id=7, name='SMA', line_type='MA', function=talib.SMA)
    EMA: Line = Line(id=8, name='EMA', line_type='MA', function=talib.EMA)
    WMA: Line = Line(id=9, name='WMA', line_type='MA', function=talib.WMA)
    DEMA: Line = Line(id=10, name='DEMA', line_type='MA', function=talib.DEMA)
    TEMA: Line = Line(id=11, name='TEMA', line_type='MA', function=talib.TEMA)
    TRIMA: Line = Line(id=12, name='TRIMA', line_type='MA', function=talib.TRIMA)
    KAMA: Line = Line(id=13, name='KAMA', line_type='MA', function=talib.KAMA)
    T3: Line = Line(id=14, name='T3', line_type='MA', function=talib.T3)

    @classmethod
    def read_many_lines(cls) -> list[Line]:
        return [
            getattr(cls, i) for i in cls.__annotations__ if isinstance(getattr(cls, i), Line)
        ]

    @classmethod
    def read_many_moving_avergaes(cls) -> list[dict]:
        return [
            {'id' : i.id, 'name' : i.name} for i in cls.read_many_lines() if i.line_type == 'MA'
        ]

