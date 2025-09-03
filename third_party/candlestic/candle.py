from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen= True)
class Candle:
    open : float
    high : float
    low : float
    close : float
    datetime : datetime

    def is_bearish(self) -> bool:
        return self.open > self.close

    def is_bullish(self) -> bool:
        return self.close > self.open

    def candle_len(self) -> float:
        return self.__len__()

    def candle_body_len(self) -> float:
        return abs(self.open - self.close)

    def to_tuple(self) -> tuple[float, float, float, float, datetime]:
        return (self.open, self.high, self.low, self.close, self.datetime)

    def __str__(self):
        return f"date-time: {self.datetime} o: {self.open} h: {self.high} l: {self.low} c: {self.close} "

    def __repr__(self):
        return f'date-time= {self.datetime} open= {self.open} high= {self.high} low= {self.low} close= {self.close}\n'

    def __len__(self):
        return self.high - self.low

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other):
        return (self.open == other.open and
                self.high == other.high and
                self.low == other.low and
                self.close == other.close)



