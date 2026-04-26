from backtrader.indicators import Indicator, AverageTrueRange,TrueRange

class TrexCandleType(Indicator):
    params = (
        ('atr_period', 16)
    )

    lines = ('candle_type',)

    def __init__(self):
        atr = AverageTrueRange(period=self.p.atr_period)
        tr = TrueRange()
        ratio = tr / atr

        self.lines.candle_type = [self._get_candle_type(i) for i in ratio]

    def _get_candle_type(self, ratio):
        if ratio < 0.8:
            return 0
        elif 0.8 <= ratio <= 1.2:
            return 1
        elif 1.2 < ratio < 2.4:
            return 2
        elif 2.4 <= ratio:
            return 3
        else:
            raise ValueError('The ratio value is out of range or wrong type')
