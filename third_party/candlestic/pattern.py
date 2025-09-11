from dataclasses import dataclass
from typing import Sequence

from third_party.candlestic import Symbol, Candle, TimeFrame


@dataclass
class Pattern:
    symbol : Symbol
    candles : Sequence[Candle]
    timestamp : TimeFrame

