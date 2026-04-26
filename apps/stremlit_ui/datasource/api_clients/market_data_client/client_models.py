from dataclasses import dataclass, asdict
from datetime import datetime
import json
from typing_extensions import TypedDict


@dataclass
class BrokerModel:
    name : str
    id : int | None = None

    def to_dict(self, without_id : bool = False):
        d = asdict(self)
        if without_id:
            d.pop('id')
        return d

    @classmethod
    def from_dict(cls, d : dict):
        return BrokerModel(**d)

@dataclass
class SymbolModel:
    name : str
    id : int | None = None

    def to_dict(self, without_id : bool = False):
        d = asdict(self)
        if without_id:
            d.pop('id')
        return d

    @classmethod
    def from_dict(cls, d : dict):
        return SymbolModel(**d)

@dataclass
class TimeFrameModel:
    name : str
    resolution : int
    id : int | None = None

    def to_dict(self, without_id : bool = False):
        d = asdict(self)
        if without_id:
            d.pop('id')
        return d

    @classmethod
    def from_dict(cls, d : dict):
        return TimeFrameModel(**d)

@dataclass
class CandleModel:
    symbol_id : int
    time_frame_id : int
    broker_id : int
    date_time : datetime
    open_ : float
    high : float
    low : float
    close : float
    volume : float
    id : int | None = None


    def to_dict(self, without_id : bool = False):
        d = asdict(self)
        if without_id:
            d.pop('id')
        d['open'] = d.pop('open_')
        return d

    @classmethod
    def from_dict(cls, d : dict):
        return CandleModel(**d)

@dataclass
class ReadManyCandlesRequest:
    time_frame_id : int
    broker_id : int
    symbol_id : int

    def to_dict(self):
        d = asdict(self)
        return d
