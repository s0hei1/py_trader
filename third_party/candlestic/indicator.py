from datetime import datetime
from typing import Callable, Sequence, Tuple

from third_party.candlestic.candle import Candle

IndicatorValue = Tuple[datetime, float | None]
CalculatorMethod = Callable[[Sequence[Candle]],Sequence[IndicatorValue]]

class BaseIndicator:

    def __init__(self,indicator_name : str,calculate_method : CalculatorMethod):
        self.indicator_name = indicator_name
        self.calculate_method = calculate_method


    def calculate(self, candles : Sequence[Candle]) -> Sequence[IndicatorValue]:
        result = self.calculate_method(candles)

        return result